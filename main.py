#!/usr/bin/env python

from bibles.asv import ASV
from bibles.esv import ESV
from bibles.kjv import KJV
from bibles.passage import PassageInvalid
from navigate import Navigate, NavigateRel, NavigateVersion
from flask import Flask, render_template, session, url_for, redirect
from flask_bootstrap import Bootstrap
from typing import List
import sys
import re


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b^lC08A7d@z3'
    bootstrap = Bootstrap(app)

    # Read the ESV API key
    try:
        with open("esv-api-key.txt", "r") as key_in:
            key = key_in.read()
            if key != "<key-goes-here>":
                api_key = key
            else:
                api_key = "unauthed"
    except IOError:
        try:
            api_key = sys.argv[1]
        except IndexError:
            api_key = "unauthed"

    esv_obj = ESV() if not len(api_key) else ESV((True, api_key))

    # JSON Bibles
    kjv_obj = KJV()
    asv_obj = ASV()

    bibles = {'ASV': asv_obj, 'ESV': esv_obj, 'KJV': kjv_obj}

    books = esv_obj.books

    debug = False

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index.html', methods=['GET', 'POST'])
    def main_page():
        """
        Main page for selecting version(s) and passage
        :return: Main menu page
        """
        choices = [book.title for book in books]
        type_sel = 'Select book'

        error_mess = None
        form = Navigate(choices=choices)
        version_select = NavigateVersion()

        if form.validate_on_submit():
            book = form.select_book.data
            versions = version_select.data
            session['select_version'] = versions
            session['select_book'] = book
            session['select_chapter'] = form.select_chapter.data

            chapter_count = 1
            for index in books:
                if index.title == book:
                    chapter_count = index.chapter_count
                    break

            chapters: List[int] = [x for x in range(1, chapter_count + 1)]
            form = Navigate(choices=chapters)
            if (session['select_chapter'] and form.submit_chapter.data and
                esv_obj.has_passage(session['select_book'], int(session['select_chapter']))) and \
                    len(versions['select_version']) == 1:
                return redirect(url_for('chapter'))
            elif (session['select_chapter'] and form.submit_chapter.data and
                  esv_obj.has_passage(session['select_book'], int(session['select_chapter']))) and \
                    len(versions['select_version']) > 1:
                return redirect(url_for('chapter_split'))
            elif form.submit_chapter.data:
                error_mess = "Please submit the book first"
        html = render_template('index.html', title='Home', formtitle='ESV Web', select_book=type_sel, books=choices,
                               debug=debug, form=form, error_mess=error_mess, version_select=version_select)
        return re.sub(r'<!--(.*?)-->|(\s{2,}\B)|\n', '', html)

    @app.route('/chapter', methods=['GET', 'POST'])
    @app.route('/chapter.html', methods=['GET', 'POST'])
    def chapter():
        """
        Reading view of a passage in a selected version
        :return: Page of the selected passage
        """
        book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
        chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"

        form = NavigateRel()

        if form.validate_on_submit():
            if form.next_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

            book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
            chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"
        version_sel = session.get('select_version')['select_version'][0] if session.get('select_version') else 'ESV'

        if version_sel in bibles.keys():
            try:
                content = bibles[version_sel].get_passage(book_sel, int(chapter_sel))
            except PassageInvalid:
                return redirect(url_for("404.html"))
        else:
            content = {"book": "Invalid version", "chapter": "",
                       "verses": {"": ["Please clear your cookies and try again"]}}

        html = render_template('chapter.html', title='Reading', formtitle='ESV Web', debug=debug, form=form,
                               content=content, version=version_sel)
        return re.sub(r'<!--(.*?)-->|(\s{2,}\B)|\n', '', html)

    @app.route('/chapter_split', methods=['GET', 'POST'])
    @app.route('/chapter_split.html', methods=['GET', 'POST'])
    def chapter_split():
        """
        Split between selected versions
        :return: Split view page of a passage in selected versions
        """
        book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
        chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"

        form = NavigateRel()

        if form.validate_on_submit():
            if form.next_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

            book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
            chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"
        version_sel = session.get('select_version')['select_version'] if session.get('select_version') else ['ESV',
                                                                                                             'KJV']
        content = []
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
        html = render_template('chapter_split.html', title=book_sel + " " + chapter_sel, formtitle='ESV Web',
                               debug=debug, form=form, content=content, version=version_sel)
        return re.sub(r'<!--(.*?)-->|(\s{2,}\B)|\n', '', html)

    @app.route('/copyright', methods=['GET'])
    @app.route('/copyright.html', methods=['GET'])
    def copyright_notice():
        """
        Copyright notice page
        :return: Copyright notice
        """
        return re.sub(r'<!--(.*?)-->|(\s{2,}\B)|\n', '', render_template("copyright.html", debug=debug))

    @app.errorhandler(500)
    def server_error(e):
        """
        Error 500 handler
        :param e: error
        :return: error 500 page
        """
        str(e)
        return re.sub(r'<!--(.*?)-->|(\s{2,}\B)|\n', '', render_template("500.html")), 500

    @app.errorhandler(404)
    def not_found(e):
        """
        Error 404 handler
        :param e: error
        :return: error 404 page
        """
        print(str(e))
        return re.sub(r'<!--(.*?)-->|(\s{2,}\B)|\n', '', render_template("404.html")), 404

    @app.route('/health', methods=['GET'])
    def health():
        """
        Docker Health check
        :return: "Healthy: OK"
        """
        return "Healthy: OK"

    return app


if __name__ == '__main__':
    # Dev start is also: `flask --app main.py run`
    app_create = create_app()
    app_create.run()
    # serve(app, host="0.0.0.0", port=5000)
