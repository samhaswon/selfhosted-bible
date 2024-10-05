#!/usr/bin/env python

# Bible + Exception Imports
from bibles import *
from multi_bible_search import BibleSearch

# Internal imports
from compress import Compress
from navigate import NavigatePassage, NavigateRel, NavigateVersion

from flask import Flask, jsonify, render_template, redirect, Response, session, url_for, request, abort, make_response
from functools import cache
from hashlib import sha256
from itertools import zip_longest
from random import randint
import re
import sys
import time
from typing import Tuple, Union

DEBUG = False


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = sha256(time.localtime().__str__().encode("utf-8")).__str__()
    Compress(app)

    if DEBUG:
        app.jinja_env.auto_reload = True

    minify = re.compile(r'<!--.*?-->|(\s{2,}\B)|\n')

    start = time.perf_counter()

    searcher = BibleSearch()
    # Read the ESV API key
    api_key: str = ""
    try:
        with open("esv-api-key.txt", "r") as key_in:
            key: str = key_in.read()
            if key != "<key-goes-here>":
                api_key = key
    except IOError:
        # This is mostly for testing
        try:
            api_key = sys.argv[1]
        except IndexError:
            pass

    bibles = {
              'ACV': ACV(),
              'AKJV': AKJV(),
              'AMP': AMP(),
              'ASV': ASV(),
              'BBE': BBE(),
              'BSB': BSB(),
              'CSB': CSB(),
              'Darby': Darby(),
              'DRA': DRA(),
              'EBR': EBR(),
              'ESV': ESV() if not len(api_key) else ESV(api_key),
              'GNV': GNV(),
              'KJV': KJV(),
              'KJV 1611': KJV1611(),
              'LSV': LSV(),
              'MSG': MSG(),
              'NASB 1995': NASB1995(),
              'NET': NET(),
              'NIV 1984': NIV1984(),
              'NIV 2011': NIV2011(),
              'NKJV': NKJV(),
              'NLT': NLT(),
              'RNKJV': RNKJV(),
              'RSV': RSV(),
              'RWV': RWV(),
              'UKJV': UKJV(),
              'WEB': WEB(),
              'YLT': YLT()
              }

    end = time.perf_counter()
    print(f"Loaded Bibles and search in {end - start:.6f} seconds")

    """
    # Fix for session expiry
    @app.before_request
    def make_session_permanent():
        session.permanent = True
    """

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index.html', methods=['GET', 'POST'])
    def main_page() -> Union[str, Response]:
        """
        Main page for selecting version(s) and passage
        :return: Main menu page
        """
        error_mess = None
        form = NavigatePassage()
        version_select = NavigateVersion()

        if form.validate_on_submit():
            session['select_version'] = versions = version_select.select_version.data
            session['select_book'] = book = form.book.data
            session['select_chapter'] = chapter_dat = form.chapter.data

            if chapter_dat and form.chapter.data and \
                    bibles['KJV'].has_passage(book, int(chapter_dat)):
                if len(versions) == 1:
                    return redirect(url_for('chapter'))
                elif len(versions) > 1:
                    return redirect(url_for('chapter_split'))
                else:
                    return abort(400)
            elif form.chapter.data:
                error_mess = "Please submit the book first"
        html: str = render_template('index.html', title='Home', debug=DEBUG, form=form, error_mess=error_mess,
                                    version_select=version_select, book=session.get('select_book', 'Genesis'),
                                    chapter=session.get('select_chapter', '1'))
        return minify.sub('', html)

    @app.route('/chapter', methods=['GET', 'POST'])
    @app.route('/chapter.html', methods=['GET', 'POST'])
    def chapter() -> Union[str, Response]:
        """
        Reading view of a passage in a selected version
        :return: Page of the selected passage
        """
        book_sel: str = session.get('select_book') if session.get('select_book') is not None else "Genesis"
        chapter_sel: str = session.get('select_chapter') if session.get('select_chapter') else "1"

        form = NavigateRel()

        passage_form = NavigatePassage()
        passage_form.book.default = book_sel

        version_select = NavigateVersion()

        if form.validate_on_submit():
            if form.next_button.data:
                form.next_button.data = False
                session['select_book'], session['select_chapter'] = bibles['KJV'].next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                form.previous_button.data = False
                session['select_book'], session['select_chapter'] = bibles['KJV'].previous_passage(book_sel, chapter_sel)

            book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
            chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"

        if passage_form.validate_on_submit() and passage_form.submit.data:
            passage_form.submit.data = False
            session['select_book'] = book_sel = passage_form.book.data
            session['select_chapter'] = chapter_sel = passage_form.chapter.data

            if len(version_select.data['select_version']) > 1 and isinstance(version_select.data['select_version'], list):
                session['select_version'] = version_select.select_version.data
                return redirect(url_for('chapter_split'))
            else:
                session['select_version'] = version_select.select_version.data

        version_sel: list = session.get('select_version')[0] if \
            session.get('select_version') else 'ESV'

        version_select.select_version.data = [version_sel]

        if version_sel in bibles.keys():
            try:
                content: dict = bibles[version_sel].get_passage(book_sel, int(chapter_sel))
            except PassageInvalid or ValueError:
                return abort(400)
        else:
            content = {"book": "Invalid version", "chapter": "",
                       "verses": {"": ["Please clear your cookies and try again"]}}

        html = render_template('chapter.html', title=book_sel + " " + chapter_sel, debug=DEBUG, form=form,
                               content=content, version=version_sel, passage_form=passage_form,
                               version_select=version_select)
        return minify.sub('', html)

    @app.route('/chapter_split', methods=['GET', 'POST'])
    @app.route('/chapter_split.html', methods=['GET', 'POST'])
    def chapter_split() -> Union[str, Response]:
        """
        Split between selected versions
        :return: Split view page of a passage in selected versions
        """
        book_sel: str = session.get('select_book') if session.get('select_book') is not None else "Genesis"
        chapter_sel: str = session.get('select_chapter') if session.get('select_chapter') else "1"

        form = NavigateRel()

        passage_form = NavigatePassage()
        passage_form.book.default = book_sel

        version_select = NavigateVersion()

        if form.validate_on_submit():
            if form.next_button.data:
                form.next_button.data = False
                session['select_book'], session['select_chapter'] = bibles['KJV'].next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                form.previous_button.data = False
                session['select_book'], session['select_chapter'] = bibles['KJV'].previous_passage(book_sel, chapter_sel)

            book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
            chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"

        if passage_form.validate_on_submit() and passage_form.submit.data:
            passage_form.submit.data = False
            session['select_book'] = book_sel = passage_form.book.data
            session['select_chapter'] = chapter_sel = passage_form.chapter.data

            if len(version_select.data['select_version']) == 1 or isinstance(version_select.data['select_version'], str):
                session['select_version'] = version_select.select_version.data
                return redirect(url_for('chapter'))
            else:
                session['select_version'] = version_select.select_version.data

        version_sel: list = session.get('select_version') if session.get('select_version') \
            else ['ESV', 'KJV']

        version_select.select_version.data = version_sel

        content: list = []
        for version in version_sel:
            if version in bibles.keys():
                try:
                    tmp_content = bibles[version].get_passage(book_sel, int(chapter_sel))
                    content.append([verse for heading, verses in tmp_content.get('verses').items() for verse in verses])
                except PassageInvalid or ValueError:
                    return abort(400)
            else:
                content.append(["Invalid version", "Please clear your cookies and try again"])
        content = list(zip_longest(*content, fillvalue=""))
        html = render_template('chapter_split.html', title=book_sel + " " + chapter_sel, debug=DEBUG, form=form,
                               content=content, chapter_num=chapter_sel, version=version_sel, passage_form=passage_form,
                               version_select=version_select, book=book_sel)
        return minify.sub('', html)

    @cache
    @app.route('/grid', methods=['GET'])
    @app.route('/grid.html', methods=['GET'])
    def grid() -> Response:
        """
        A grid of Bible passages.
        :return: HTML page of iframes for Bible passages.
        """
        response = make_response(minify.sub('', render_template("grid.html", debug=DEBUG, versions=bibles.keys())))
        response.cache_control.max_age = 60 * 60 * 24 * 7
        return response # minify.sub('', render_template("grid.html", debug=debug, versions=bibles.keys()))

    @cache
    @app.route('/copyright', methods=['GET'])
    @app.route('/copyright.html', methods=['GET'])
    def copyright_notice() -> Response:
        """
        Copyright notice page
        :return: Copyright notice
        """
        response = make_response(minify.sub('', render_template("copyright.html", debug=DEBUG)))
        response.cache_control.max_age = 60 * 60 * 24 * 7
        response.cache_control.public = True
        return response

    @app.route('/chapters/<book>', methods=['GET'])
    def chapters(book) -> Response:
        """
        Get the number of chapters for the given book.
        :param book: Book to get the chapters of.
        :return: JSON object of the format {"num_chapters": int}
        """
        try:
            num_chapters = bibles['KJV'].books_of_the_bible[book]
        except KeyError:
            num_chapters = 1
        # return the number of chapters as a JSON response
        return jsonify({'num_chapters': num_chapters})

    @app.route('/embed', methods=['GET'])
    def embed() -> Response:
        """
        Generate passage embeddings for the grid of passages.
        :return: The HTML for the iframe.
        """
        # Get the parameters
        version = request.args.get('version', 'ESV')
        book = request.args.get('book', 'Genesis')
        chapter_ref = request.args.get('chapter', '1')

        # Get the passage, returning 400 for invalid references
        try:
            content: dict = bibles[version].get_passage(book, int(chapter_ref))
        except PassageInvalid or ValueError or KeyError:
            return abort(400)
        response = make_response(minify.sub('', render_template('embed.html', title=book + " " + chapter_ref, debug=DEBUG,
                               content=content, version=version)))
        response.cache_control.max_age = 60 * 60 * 24 * 7
        return response

    @app.route('/goto/', methods=['GET'])
    def goto() -> Response:
        """
        Go to a passage as specified by the query parameters.
        :return: Redirect to the chapter page.
        """
        # Get the parameters
        version = request.args.get('version', 'ESV')
        book = request.args.get('book', 'Genesis')
        chapter_ref = request.args.get('chapter', '1')

        # Use those for the session, validated elsewhere.
        session['select_version'] = [version]
        session['select_book'], session['select_chapter'] = book, chapter_ref
        return redirect(url_for("chapter"))

    @app.route('/search_endpoint/', methods=['GET'])
    def search_endpoint() -> Response:
        """
        Endpoint queried by the frontend search.
        :return: Search results with references and verse content.
        """
        version = request.args.get('version')
        query = request.args.get('query')

        if version not in bibles.keys():
            return abort(400)

        # Make sure the query is a reasonable length (max is 528 in the KJV for reference).
        if len(query) > 700:
            query = query[:700]

        results = searcher.search(query, version=version, max_results=100)
        references = {}
        for result in results:
            space_index = result.rfind(" ")
            colon_index = result.rfind(":")
            book, chapter_ref, verse_ref = \
                result[0:space_index], int(result[space_index:colon_index]), result[colon_index + 1:] + " "

            verses = bibles[version].get_passage(book, chapter_ref)['verses']
            for heading in verses.keys():
                for verse in verses[heading]:
                    if verse.startswith(verse_ref):
                        if result in references:
                            references[result] += verse[verse.find(" ") + 1:]
                        else:
                            references[result] = verse[verse.find(" ") + 1:]
        reference_list = [(ref, val) for ref, val in references.items()]
        return jsonify({'results': reference_list})

    @cache
    @app.route('/search', methods=['GET'])
    def search() -> Response:
        response = make_response(minify.sub('', render_template('search.html', title='search', debug=DEBUG, versions=bibles.keys())))
        response.cache_control.max_age = 60 * 60 * 24 * 7
        return response

    @app.route('/500', methods=['GET'])
    @app.errorhandler(500)
    def server_error(e=None) -> Tuple[str, int]:
        """
        Error 500 handler
        :param e: error
        :return: error 500 page
        """
        str(e)
        return (minify.sub('',
                          render_template("500.html",
                                          image=f"500_im_{randint(1, 5)}.jpg")),
                500)

    @app.route('/404', methods=['GET'])
    @app.errorhandler(404)
    def not_found(e = "") -> Tuple[str, int]:
        """
        Error 404 handler
        :param e: error
        :return: error 404 page
        """
        str(e)
        return minify.sub('', render_template("404.html")), 404

    @app.route('/400', methods=['GET'])
    @app.errorhandler(400)
    def bad_request(e="") -> Tuple[str, int]:
        """
        Error 400 handler
        :param e: error
        :return: error 400 page
        """
        str(e)
        return minify.sub('', render_template("400.html")), 400

    @app.errorhandler(414)
    def request_too_long(e) -> Tuple[str, int]:
        """
        Error 414 handler
        :param e: error
        :return: error 414 page
        """
        str(e)
        return minify.sub('', render_template("414.html")), 414

    @app.route('/health', methods=['GET'])
    def health() -> str:
        """
        Docker Health check
        :return: "Healthy: OK"
        """
        return "Healthy: OK"

    return app


if __name__ == '__main__':
    DEBUG = True
    # Dev start is also: `flask --app main.py run`
    app_create: Flask = create_app()
    app_create.run()
    # serve(app, host="0.0.0.0", port=5000)
