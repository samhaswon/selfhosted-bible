#!/usr/bin/env python

from esv import ESV
from book import Book
from navigate import Navigate, SelectChapter
from flask import Flask, render_template, session, request, url_for, redirect
from flask_bootstrap import Bootstrap
from bokeh.resources import INLINE
from typing import List
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b^lC08A7d@z3'
bootstrap = Bootstrap(app)

books = ESV(False).books


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def main_page():
    # setup
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = None, None
    debug = False

    choices = [book.title for book in books]
    type_sel = 'Select book'

    if request.method == 'GET':
        session.clear()
    session['select_book'] = None
    session['select_chapter'] = None
    form = Navigate(choices=choices)

    if form.validate_on_submit():
        book = form.select_book.data
        print(book)

        chapter_count = 1
        for index in books:
            if index.title == book:
                chapter_count = index.chapter_count
                break

        chapters: List[int] = [x for x in range(1, chapter_count + 1)]
        form = Navigate(choices=chapters)

    html = render_template('index.html', title='Home', formtitle='ESV Web', select_book=type_sel,
                           books=choices, plot_script=script, debug=debug, form=form,
                           plot_div=div, js_resources=js_resources, css_resources=css_resources)
    return html


@app.route('/chapter', methods=['GET', 'POST'])
@app.route('/chapter.html', methods=['GET', 'POST'])
def chapter():
    # setup
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    book = session.get('book_selection')

    html = render_template('chapter.html', title='Home')
    return html


if __name__ == '__main__':
    app.run()
