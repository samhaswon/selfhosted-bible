#!/usr/bin/env python

from esv import ESV
from navigate import Navigate, NavigateRel
from flask import Flask, render_template, session, url_for, redirect
from flask_bootstrap import Bootstrap
from typing import List
import sys


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b^lC08A7d@z3'
    bootstrap = Bootstrap(app)

    try:
        api_key = open("api-key.txt", "r").read()
    except IOError:
        try:
            api_key = sys.argv[1]
        except IndexError:
            api_key = ""

    esv_obj = None

    if len(api_key):
        esv_obj = ESV(False)
    else:
        esv_obj = ESV(False, (True, api_key))
    books = esv_obj.books

    debug = False

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index.html', methods=['GET', 'POST'])
    def main_page():

        choices = [book.title for book in books]
        type_sel = 'Select book'

        error_mess = None
        form = Navigate(choices=choices)

        if form.validate_on_submit():
            book = form.select_book.data
            session['select_book'] = book
            session['select_chapter'] = form.select_chapter.data

            chapter_count = 1
            for index in books:
                if index.title == book:
                    chapter_count = index.chapter_count
                    break

            chapters: List[int] = [x for x in range(1, chapter_count + 1)]
            form = Navigate(choices=chapters)
            if session['select_chapter'] and form.submit_chapter.data and esv_obj.has_passage(session['select_book'], int(session['select_chapter'])):
                # if esv_obj.has_passage(session['select_book'], int(session['select_chapter'])):
                return redirect(url_for('chapter'))
            elif form.submit_chapter.data:
                error_mess = "Please submit the book first"
        html = render_template('index.html', title='Home', formtitle='ESV Web', select_book=type_sel, books=choices,
                               debug=debug, form=form, error_mess=error_mess)
        return html

    @app.route('/chapter', methods=['GET', 'POST'])
    @app.route('/chapter.html', methods=['GET', 'POST'])
    def chapter():
        book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
        chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"
        if not esv_obj.has_passage(book_sel, int(chapter_sel)):
            return redirect(url_for("404.html"))

        form = NavigateRel()

        if form.validate_on_submit():
            if form.next_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.next_passage(book_sel, chapter_sel)
            elif form.previous_button.data:
                session['select_book'], session['select_chapter'] = esv_obj.previous_passage(book_sel, chapter_sel)

        book_sel = session.get('select_book') if session.get('select_book') is not None else "Genesis"
        chapter_sel = session.get('select_chapter') if session.get('select_chapter') else "1"

        content = esv_obj.get_passage(book_sel, int(chapter_sel))

        html = render_template('chapter.html', title='Reading', formtitle='ESV Web', debug=debug,
                               form=form, content=content)
        return html

    @app.route('/copyright', methods=['GET'])
    @app.route('/copyright.html', methods=['GET'])
    def copyright_notice():
        return render_template("copyright.html", title="ESV Copyright Notice", debug=debug,)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    return app


if __name__ == '__main__':
    # Dev start is also: `flask --app main.py run`
    app = create_app()
    app.run()
    # serve(app, host="0.0.0.0", port=5080)
