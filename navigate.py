from wtforms import SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_wtf import FlaskForm
from typing import List, Tuple
from esv import ESV


class Navigate(FlaskForm):
    books = ESV().books
    choices: List[str] = [book.title for book in books]

    select_chapter = SelectField('Select chapter', choices=[], validators=[Optional()])
    select_book = SelectField('Select book', choices=choices, coerce=str, validators=[DataRequired()])
    submit_book = SubmitField('Submit book')
    submit_chapter = SubmitField('Submit chapter')

    def __init__(self, choices: list, *args, **kwargs):
        super(Navigate, self).__init__(*args, **kwargs)
        self.select_chapter.choices = choices if type(choices[0]) is int else []
