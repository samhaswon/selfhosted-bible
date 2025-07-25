"""
Authors: William Fagan, Samuel Howard
Copyright (c) 2013-2017 William Fagan
License: The MIT License (MIT)
"""
from gzip import GzipFile
from io import BytesIO
from typing import Union, List
import zlib

import brotli
from flask import request


class Compress:
    """
    The Compress object allows your application to use Flask-Compress.

    When initializing a Compress object, you may optionally provide your
    :class:`flask.Flask` application object if it is ready. Otherwise,
    you may provide it later by using the :meth:`init_app` method.

    :param app: (Optional) :class:`flask.Flask` application object.
    :type app: :class:`flask.Flask` or None
    """
    def __init__(self, app = None) -> None:
        """
        An alternative way to pass your :class:`flask.Flask` application
        object to Flask-Compress. :meth:`init_app` also takes care of some
        default `settings`_.

        :param app: the :class:`flask.Flask` application object.
        """
        self.enabled_algorithms: list = []
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app) -> None:
        """
        Enables this module for the given app.
        :param app: The app to enable compression for.
        :return: None.
        """
        defaults: List[tuple] = [
            ('COMPRESS_MIMETYPES', ['text/html', 'text/css', 'text/xml', 'application/json',
                                    'application/javascript', 'image/x-icon', 'image/svg+xml']),
            ('COMPRESS_LEVEL', 6),
            ('COMPRESS_BR_LEVEL', 4),
            ('COMPRESS_BR_MODE', 0),
            ('COMPRESS_BR_WINDOW', 22),
            ('COMPRESS_BR_BLOCK', 0),
            ('COMPRESS_DEFLATE_LEVEL', -1),
            ('COMPRESS_MIN_SIZE', 500),
            ('COMPRESS_CACHE_KEY', None),
            ('COMPRESS_CACHE_BACKEND', None),
            ('COMPRESS_REGISTER', True),
            ('COMPRESS_STREAMS', True),
            ('COMPRESS_ALGORITHM', ['br', 'gzip', 'deflate']),
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        self.enabled_algorithms = app.config['COMPRESS_ALGORITHM']

        if (app.config['COMPRESS_REGISTER'] and
                app.config['COMPRESS_MIMETYPES']):
            app.after_request(self.after_request)

    def _choose_compress_algorithm(self, accept_encoding_header) -> Union[str, None]:
        """
        Determine which compression algorithm we're going to use based on the
        client request. The `Accept-Encoding` header may list one or more desired
        algorithms, together with a "quality factor" for each one (higher quality
        means the client prefers that algorithm more).

        :param accept_encoding_header: `Accept-Encoding` header's content.
        :return: Name of a compression algorithm (`gzip`, `deflate`, `br`) or `None` if
            the client and server don't agree on any.
        """
        # A flag denoting that client requested to use any (`*`) algorithm,
        # in case the server does not support a specific one
        fallback_to_any: bool = False

        # Map quality factors to the requested algorithm names.
        algos_by_quality: dict = {}

        for part in accept_encoding_header.lower().split(','):
            part = part.strip()
            if ';q=' in part:
                # If the client associated a quality factor with an algorithm,
                # try to parse it. We could do the matching using a regex, but
                # the format is so simple that it is overkill to do so.
                algo = part.split(';')[0].strip()
                try:
                    quality = float(part.split('=')[1].strip())
                except ValueError:
                    quality = 1.0
            else:
                # Otherwise, use the default quality
                algo = part
                quality = 1.0

            if algo == '*' and quality > 0:
                fallback_to_any = True
            elif algo == 'identity':  # identity means 'no compression asked'
                algos_by_quality[str(quality)] = None
            elif algo in self.enabled_algorithms:
                algos_by_quality[str(quality)] = algo

        # Choose the algorithm with the highest quality factor that the server supports.
        #
        # If there are multiple equally good options, choose the first supported algorithm
        # from server configuration.
        #
        # If the server doesn't support any algorithm that the client requested but
        # there's a special wildcard algorithm request (`*`), choose the first supported
        # algorithm.
        for _, viable_algos in sorted(algos_by_quality.items(), reverse=True):
            if len(viable_algos) == 1:
                return viable_algos.pop()
            if len(viable_algos) > 1:
                for server_algo in self.enabled_algorithms:
                    if server_algo in viable_algos:
                        return server_algo

        return self.enabled_algorithms[0] if fallback_to_any else None

    def after_request(self, response):
        """
        Choose the appropriate algorithm to compress the response with,
        then return the compressed response.
        :param response: The response to compress.
        :return: The compressed response.
        """
        vary = response.headers.get('Vary')
        if not vary:
            response.headers['Vary'] = 'Accept-Encoding'
        elif 'accept-encoding' not in vary.lower():
            response.headers['Vary'] = f"{vary}, Accept-Encoding"

        accept_encoding = request.headers.get('Accept-Encoding', '')
        chosen_algorithm = self._choose_compress_algorithm(accept_encoding)

        # pylint: disable=too-many-boolean-expressions
        if (not chosen_algorithm or
            response.mimetype not in self.app.config["COMPRESS_MIMETYPES"] or
            response.status_code < 200 or
            response.status_code >= 300 or
            (response.is_streamed and not self.app.config["COMPRESS_STREAMS"]) or
            "Content-Encoding" in response.headers or
            (not response.content_length and
             response.content_length < self.app.config["COMPRESS_MIN_SIZE"])):
            return response

        response.direct_passthrough = False

        compressed_content = self.compress(self.app, response, chosen_algorithm)

        response.set_data(compressed_content)

        response.headers['Content-Encoding'] = chosen_algorithm
        response.headers['Content-Length'] = response.content_length

        if response.mimetype != 'text/html':
            response.cache_control.max_age = 60 * 60 * 24 * 7
            response.cache_control.public = True
            response.cache_control.no_cache = None

        # "123456789"   => "123456789:gzip"   - A strong ETag validator
        # W/"123456789" => W/"123456789:gzip" - A weak ETag validator
        if etag := response.headers.get('ETag'):
            response.headers['ETag'] = f'{etag[:-1]}:{chosen_algorithm}"'

        return response

    # pylint: disable=inconsistent-return-statements
    @staticmethod
    def compress(app, response, algorithm) -> bytes:
        """
        Compress the given response with the given algorithm.
        :param app: This app.
        :param response: The response to compress.
        :param algorithm: The algorithm used.
        :return: The compressed version of the response.
        """
        if algorithm == 'gzip':
            gzip_buffer = BytesIO()
            with GzipFile(mode='wb',
                          compresslevel=app.config['COMPRESS_LEVEL'],
                          fileobj=gzip_buffer) as gzip_file:
                gzip_file.write(response.get_data())
            return gzip_buffer.getvalue()
        if algorithm == 'deflate':
            return zlib.compress(response.get_data(),
                                 app.config['COMPRESS_DEFLATE_LEVEL'])
        if algorithm == 'br':
            return bytes(brotli.compress(response.get_data(),
                                   mode=app.config['COMPRESS_BR_MODE'],
                                   quality=app.config['COMPRESS_BR_LEVEL'],
                                   lgwin=app.config['COMPRESS_BR_WINDOW'],
                                   lgblock=app.config['COMPRESS_BR_BLOCK']))
