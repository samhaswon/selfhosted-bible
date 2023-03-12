from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from typing import List
from bibles.esv import ESV


class NonValidatingSelectField(SelectField):
    """
    Class to ignore the SelectField validation
    """
    def pre_validate(self, form):
        """
        Does nothing
        :param form: form to validate
        :return: None
        """
        pass


class Navigate(FlaskForm):
    books = ESV().books
    choices: List[str] = [book.title for book in books]

    select_chapter = NonValidatingSelectField('Select chapter', choices=[], validators=[Optional()])
    select_book = SelectField('Select book', choices=choices, coerce=str, validators=[DataRequired()])
    submit_book = SubmitField('Submit book')
    submit_chapter = SubmitField('Submit chapter')

    def __init__(self, choices: list, *args, **kwargs):
        super(Navigate, self).__init__(*args, **kwargs)
        self.select_chapter.choices = choices if type(choices[0]) is int else []


class NavigateRel(FlaskForm):
    next_button = SubmitField("Next")
    previous_button = SubmitField("Previous")
