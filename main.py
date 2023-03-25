#!/usr/bin/env python

from bibles.asv import ASV
from bibles.esv import ESV
from bibles.kjv import KJV
from bibles.passage import PassageInvalid
from navigate import Navigate, NavigateRel, NavigateVersion
from flask import Flask, render_template, session, url_for, redirect, Response
from typing import List, Tuple, Union
import sys
import re


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b^lC08A7d@z3'

    minify = re.compile(r'<!--(.*?)-->|(\s{2,}\B)|\n')

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
    esv_obj = ESV() if not len(api_key) else ESV((True, api_key))

    # JSON Bibles
    kjv_obj = KJV()
    asv_obj = ASV()

    bibles = {'ASV': asv_obj, 'ESV': esv_obj, 'KJV': kjv_obj}

    debug = False

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index.html', methods=['GET', 'POST'])
    def main_page() -> Union[str, Response]:
        """
        Main page for selecting version(s) and passage
        :return: Main menu page
        """
        error_mess = None
        form = Navigate(choices=[""])
        version_select = NavigateVersion()

        if form.validate_on_submit():
            # book: str = form.select_book.data
            # versions: dict = version_select.data
            session['select_version'] = versions = version_select.data
            session['select_book'] = book = form.select_book.data
            session['select_chapter'] = chapter_dat = form.select_chapter.data

            chapter_count: int = esv_obj.chapter_count(book)

            chapters: List[int] = [x for x in range(1, chapter_count + 1)]
            form = Navigate(choices=chapters)

            if chapter_dat and form.submit_chapter.data and \
                    esv_obj.has_passage(book, int(chapter_dat)):
                if len(versions['select_version']) == 1:
                    return redirect(url_for('chapter'))
                elif len(versions['select_version']) > 1:
                    return redirect(url_for('chapter_split'))
                else:
                    return redirect(url_for("404.html"))
            elif form.submit_chapter.data:
                error_mess = "Please submit the book first"
        html: str = render_template('index.html', title='Home', debug=debug, form=form, error_mess=error_mess,
                                    version_select=version_select)
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

        if form.validate_on_submit():
            if form.next_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

            book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
            chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"
        version_sel: list = session.get('select_version')['select_version'][0] if \
            session.get('select_version') else 'ESV'

        if version_sel in bibles.keys():
            try:
                content: dict = bibles[version_sel].get_passage(book_sel, int(chapter_sel))
            except PassageInvalid:
                return redirect(url_for("404.html"))
        else:
            content = {"book": "Invalid version", "chapter": "",
                       "verses": {"": ["Please clear your cookies and try again"]}}

        html = render_template('chapter.html', title='Reading', debug=debug, form=form, content=content,
                               version=version_sel)
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

        if form.validate_on_submit():
            if form.next_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

            book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
            chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"
        version_sel: list = session.get('select_version')['select_version'] if session.get('select_version') \
            else ['ESV', 'KJV']

        content: list = []
        for version in version_sel:
            if version in bibles.keys():
                try:
                    tmp_content = bibles[version].get_passage(book_sel, int(chapter_sel))
                    content.append([verse for heading, verses in tmp_content.get('verses').items() for verse in verses])
                except PassageInvalid:
                    return redirect(url_for("404.html"))
            else:
                content.append(["Invalid version", "Please clear your cookies and try again"])
        content = list(zip(*content))
        html = render_template('chapter_split.html', title=book_sel + " " + chapter_sel, debug=debug, form=form,
                               content=content, version=version_sel)
        return minify.sub('', html)

    @app.route('/copyright', methods=['GET'])
    @app.route('/copyright.html', methods=['GET'])
    def copyright_notice() -> str:
        """
        Copyright notice page
        :return: Copyright notice
        """
        return minify.sub('', render_template("copyright.html", debug=debug))

    @app.errorhandler(500)
    def server_error(e) -> Tuple[str, int]:
        """
        Error 500 handler
        :param e: error
        :return: error 500 page
        """
        str(e)
        return minify.sub('', render_template("500.html")), 500

    @app.errorhandler(404)
    def not_found(e) -> Tuple[str, int]:
        """
        Error 404 handler
        :param e: error
        :return: error 404 page
        """
        str(e)
        return minify.sub('', render_template("404.html")), 404

    @app.route('/health', methods=['GET'])
    def health() -> str:
        """
        Docker Health check
        :return: "Healthy: OK"
        """
        return "Healthy: OK"

    return app


if __name__ == '__main__':
    # Dev start is also: `flask --app main.py run`
    app_create: Flask = create_app()
    app_create.run()
    # serve(app, host="0.0.0.0", port=5000)
