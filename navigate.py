from wtforms import SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm


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

class NavigatePassage(FlaskForm):
    books = [('Genesis', 'Genesis'),
             ('Exodus', 'Exodus'),
             ('Leviticus', 'Leviticus'),
             ('Numbers', 'Numbers'),
             ('Deuteronomy', 'Deuteronomy'),
             ('Joshua', 'Joshua'),
             ('Judges', 'Judges'),
             ('Ruth', 'Ruth'),
             ('1 Samuel', '1 Samuel'),
             ('2 Samuel', '2 Samuel'),
             ('1 Kings', '1 Kings'),
             ('2 Kings', '2 Kings'),
             ('1 Chronicles', '1 Chronicles'),
             ('2 Chronicles', '2 Chronicles'),
             ('Ezra', 'Ezra'),
             ('Nehemiah', 'Nehemiah'),
             ('Esther', 'Esther'),
             ('Job', 'Job'),
             ('Psalms', 'Psalms'),
             ('Proverbs', 'Proverbs'),
             ('Ecclesiastes', 'Ecclesiastes'),
             ('Song of Solomon', 'Song of Solomon'),
             ('Isaiah', 'Isaiah'),
             ('Jeremiah', 'Jeremiah'),
             ('Lamentations', 'Lamentations'),
             ('Ezekiel', 'Ezekiel'),
             ('Daniel', 'Daniel'),
             ('Hosea', 'Hosea'),
             ('Joel', 'Joel'),
             ('Amos', 'Amos'),
             ('Obadiah', 'Obadiah'),
             ('Jonah', 'Jonah'),
             ('Micah', 'Micah'),
             ('Nahum', 'Nahum'),
             ('Habakkuk', 'Habakkuk'),
             ('Zephaniah', 'Zephaniah'),
             ('Haggai', 'Haggai'),
             ('Zechariah', 'Zechariah'),
             ('Malachi', 'Malachi'),
             ('Matthew', 'Matthew'),
             ('Mark', 'Mark'),
             ('Luke', 'Luke'),
             ('John', 'John'),
             ('Acts', 'Acts'),
             ('Romans', 'Romans'),
             ('1 Corinthians', '1 Corinthians'),
             ('2 Corinthians', '2 Corinthians'),
             ('Galatians', 'Galatians'),
             ('Ephesians', 'Ephesians'),
             ('Philippians', 'Philippians'),
             ('Colossians', 'Colossians'),
             ('1 Thessalonians', '1 Thessalonians'),
             ('2 Thessalonians', '2 Thessalonians'),
             ('1 Timothy', '1 Timothy'),
             ('2 Timothy', '2 Timothy'),
             ('Titus', 'Titus'),
             ('Philemon', 'Philemon'),
             ('Hebrews', 'Hebrews'),
             ('James', 'James'),
             ('1 Peter', '1 Peter'),
             ('2 Peter', '2 Peter'),
             ('1 John', '1 John'),
             ('2 John', '2 John'),
             ('3 John', '3 John'),
             ('Jude', 'Jude'),
             ('Revelation', 'Revelation')]
    book = SelectField('Book', choices=books, validators=[DataRequired()])
    chapter = NonValidatingSelectField('Chapter', choices=[], validators=[Optional()])
    submit = SubmitField("Go to passage")


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
