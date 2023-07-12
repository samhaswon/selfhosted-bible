from wtforms import SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from typing import List


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
    choices: List[str] = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
                          '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
                          'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
                          'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah',
                          'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
                          'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
                          'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
                          '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
                          '1 John', '2 John', '3 John', 'Jude', 'Revelation']

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
    select_version: SelectField = SelectMultipleField('Select version',
                                                      choices=['AMP', 'ASV', 'BSB', 'CSB', 'ESV', 'GNV', 'KJV', 'LSV',
                                                               'MSG', 'NASB 1995', 'NET', 'NIV 1984', 'NIV 2011',
                                                               'NKJV', 'NLT', 'RSV', 'WEB', 'YLT'],
                                                      coerce=str, validators=[DataRequired()], default=['ESV'])
