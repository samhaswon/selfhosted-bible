from wtforms import SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from typing import List
from bibles.kjv import KJV


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
    books = KJV().books
    choices: List[str] = [book.name for book in books]

    select_chapter: SelectField = NonValidatingSelectField('Select chapter', choices=[], validators=[Optional()])
    select_book: SelectField = SelectField('Select book', choices=choices, coerce=str, validators=[DataRequired()])
    submit_book: SelectField = SubmitField('Submit book')
    submit_chapter: SelectField = SubmitField('Submit chapter')

    def __init__(self, choices: list, *args, **kwargs):
        super(Navigate, self).__init__(*args, **kwargs)
        self.select_chapter.choices = choices if type(choices[0]) is int else []


class NavigateRel(FlaskForm):
    """
    Two basic submit fields for chapter navigation
    """
    next_button: SubmitField = SubmitField("Next")
    previous_button: SubmitField = SubmitField("Previous")


class NavigateVersion(FlaskForm):
    """
    Field for selecting Bible version
    """
    select_version: SelectField = SelectMultipleField('Select version', choices=['ASV', 'ESV', 'KJV'],
                                                      coerce=str, validators=[DataRequired()], default=['ESV'])
