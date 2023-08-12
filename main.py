#!/usr/bin/env python

from bibles.akjv import AKJV
from bibles.amp import AMP
from bibles.asv import ASV
from bibles.bbe import BBE
from bibles.bsb import BSB
from bibles.csb import CSB
from bibles.esv import ESV
from bibles.gnv import GNV
from bibles.kjv import KJV
from bibles.kjv1611 import KJV1611
from bibles.lsv import LSV
from bibles.msg import MSG
from bibles.nasb1995 import NASB1995
from bibles.net import NET
from bibles.niv1984 import NIV1984
from bibles.niv2011 import NIV2011
from bibles.nkjv import NKJV
from bibles.nlt import NLT
from bibles.rsv import RSV
from bibles.web import WEB
from bibles.ylt import YLT

from bibles.passage import PassageInvalid
from navigate import NavigateRel, NavigateVersion, NavigatePassage
from flask import Flask, render_template, session, url_for, redirect, Response, jsonify
from compress import Compress
from typing import Tuple, Union
import sys
import re
import time


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b^lC08A7d@z3'
    Compress(app)

    minify = re.compile(r'<!--(.*?)-->|(\s{2,}\B)|\n')

    start = time.perf_counter()
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

    # JSON API Bibles
    esv_obj = ESV() if not len(api_key) else ESV((True, api_key))
    amp_obj = AMP()
    msg_obj = MSG()
    nasb_1995_obj = NASB1995()
    net_obj = NET()
    nkjv_obj = NKJV()
    niv_1984_obj = NIV1984()
    niv_2011_obj = NIV2011()
    nlt_obj = NLT()
    rsv_obj = RSV()

    # XML Bibles?
    csb_obj = CSB()

    # JSON Bibles
    akjv_obj = AKJV()
    bbe_obj = BBE()
    kjv_obj = KJV()
    kjv_1611_obj = KJV1611()
    asv_obj = ASV()
    bsb_obj = BSB()
    gnv_obj = GNV()
    lsv_obj = LSV()
    web_obj = WEB()
    ylt_obj = YLT()

    end = time.perf_counter()
    print(f"Loaded Bibles in {end - start} seconds")

    bibles = {'AKJV': akjv_obj, 'AMP': amp_obj, 'ASV': asv_obj, 'BBE': bbe_obj, 'BSB': bsb_obj, 'CSB': csb_obj,
              'ESV': esv_obj, 'GNV': gnv_obj, 'KJV': kjv_obj, 'KJV 1611': kjv_1611_obj, 'LSV': lsv_obj, 'MSG': msg_obj,
              'NASB 1995': nasb_1995_obj, 'NET': net_obj, 'NIV 1984': niv_1984_obj, 'NIV 2011': niv_2011_obj,
              'NKJV': nkjv_obj, 'NLT': nlt_obj, 'RSV': rsv_obj, 'WEB': web_obj, 'YLT': ylt_obj}

    debug = False

    # Fix for session expiry
    @app.before_request
    def make_session_permanent():
        session.permanent = True

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
                    esv_obj.has_passage(book, int(chapter_dat)):
                if len(versions) == 1:
                    return redirect(url_for('chapter'))
                elif len(versions) > 1:
                    return redirect(url_for('chapter_split'))
                else:
                    return redirect(url_for("404.html"))
            elif form.chapter.data:
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

        passage_form = NavigatePassage()
        passage_form.book.default = book_sel

        version_select = NavigateVersion()

        if form.validate_on_submit():
            if form.next_button.data:
                form.next_button.data = False
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                form.previous_button.data = False
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

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
            except PassageInvalid:
                return redirect(url_for("404.html"))
        else:
            content = {"book": "Invalid version", "chapter": "",
                       "verses": {"": ["Please clear your cookies and try again"]}}

        html = render_template('chapter.html', title=book_sel + " " + chapter_sel, debug=debug, form=form,
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
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                form.previous_button.data = False
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

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
                except PassageInvalid:
                    return redirect(url_for("404.html"))
            else:
                content.append(["Invalid version", "Please clear your cookies and try again"])
        content = list(zip(*content))
        html = render_template('chapter_split.html', title=book_sel + " " + chapter_sel, debug=debug, form=form,
                               content=content, chapter_num=chapter_sel, version=version_sel, passage_form=passage_form,
                               version_select=version_select)
        return minify.sub('', html)

    @app.route('/copyright', methods=['GET'])
    @app.route('/copyright.html', methods=['GET'])
    def copyright_notice() -> str:
        """
        Copyright notice page
        :return: Copyright notice
        """
        return minify.sub('', render_template("copyright.html", debug=debug))

    @app.route('/chapters/<book>')
    def chapters(book) -> Response:
        # get the number of chapters for the given book
        try:
            num_chapters = kjv_obj.books_of_the_bible[book]
        except KeyError:
            num_chapters = 1
        # return the number of chapters as a JSON response
        return jsonify({'num_chapters': num_chapters})

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
