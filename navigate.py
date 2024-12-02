from wtforms import SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm


class NonValidatingSelectField(SelectField):
    """
    Class to ignore the SelectField validation
    """

    def pre_validate(self, form) -> None:
        """
        Does nothing
        :param form: form to validate
        :return: None
        """
        pass

class NavigatePassage(FlaskForm):
    """
    FlaskForm for Bible passage navigation. Should be used with navigate.js on the frontend to make a dynamic dropdown
    for passage selection.
    """
    # Books of the Bible, as 2-tuples, for form creation.
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
    next_button: SubmitField = SubmitField(">")
    previous_button: SubmitField = SubmitField("<")


class NavigateVersion(FlaskForm):
    """
    Field for selecting a Bible version
    """
    select_version: SelectField = SelectMultipleField('Select version',
                                                      choices=[('ACV', 'A Conservative Version (ACV)'),
                                                               ('AKJV', 'American King James Version (AKJV)'),
                                                               ('AMP', 'Amplified Bible (AMP)'),
                                                               ('ASV', 'American Standard Version (ASV)'),
                                                               ('BBE', 'Bible in Basic English (BBE)'),
                                                               ('BSB', 'Berean Standard Bible (BSB)'),
                                                               ('CSB', 'Christian Standard Bible (CSB)'),
                                                               ('Darby', 'Darby Bible (Darby)'),
                                                               ('DRA', 'Douay-Rheims 1899 American Edition (DRA)'),
                                                               ('EBR', 'Rotherham\'s Emphasized Bible (EBR)'),
                                                               ('ESV', 'English Standard Version (ESV)'),
                                                               ('GNV', 'Geneva Bible (GNV)'),
                                                               ('KJV', 'King James Version (KJV, 1729)'),
                                                               ('KJV 1611', 'King James Version 1611 (KJV, 1611)'),
                                                               ('LSV', 'Literal Standard Version (LSV)'),
                                                               ('MSG', 'The Message (MSG)'),
                                                               ('NASB 1995', 'New American Standard Bible (NASB, 1995)'),
                                                               ('NET', 'New English Translation (NET)'),
                                                               ('NIV 1984', 'New International Version (NIV, 1984)'),
                                                               ('NIV 2011', 'New International Version (NIV, 2011)'),
                                                               ('NKJV', 'New King James Version (NKJV)'),
                                                               ('NLT', 'New Living Translation (NLT)'),
                                                               ('RNKJV', 'Restored Name King James Version (RNKJV)'),
                                                               ('RSV', 'Revised Standard Version (RSV)'),
                                                               ('RWV', 'Revised Webster Version 1833 (RWV)'),
                                                               ('UKJV', 'Updated King James Version (UKJV)'),
                                                               ('WEB', 'World English Bible (WEB)'),
                                                               ('YLT', 'Young’s Literal Translation (YLT)'),
                                                               ('BTX3', 'La Biblia Textual 3ra Edicion (BTX3)'),
                                                               ('RV1960', 'Reina-Valera 1960 (RV1960)'),
                                                               ('RV2004', 'Reina Valera Gómez 2004 (RV2004)')
                                                               ],
                                                      validators=[DataRequired()], default=['ESV'])
