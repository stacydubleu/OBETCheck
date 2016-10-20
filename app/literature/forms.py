# Import the Form class, fields, and validators from wtform
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import Required, Length, Optional, NumberRange, URL
#from flask.ext.pagedown.fields import PageDownField
# Import database models
from ..models import User, Lit, Role

# For for privileged users to add material into the database
class AddLitForm(Form):
    refType = SelectField('Reference Type', validators = [Required()], choices=[('Book Section','Book Section'), ('Edited Book', 'Edited Book') , ('Journal Article', 'Journal Article'), ('Journal Issue', 'Journal Issue'),('Magazine Article', 'Magazine Article'), ('Media', 'Media'), ('Newspaper Article', 'Newspaper Article'), ('Report', 'Report'), ('Thesis', 'Thesis'), ('Website', 'Website')])
    author = StringField('Author', validators = [Length(0,120)])
    title = StringField('Title', validators = [Required(), Length(1,150)])
    yrPublished = IntegerField('Year Published', validators = [NumberRange(min=1800), Optional()])  # MUST ADD max_value!!! Limit it to THIS year!!
    sourceTitle = StringField('SourceTitle', validators = [Length(0,200)])
    editor = StringField('Editor', validators = [Length(0,150)])
    placePublished = StringField('Place Published', validators = [Length(0,150)])
    publisher = StringField('Publisher', validators = [Length(0,200)])
    volume = StringField('Volume', validators = [Length(0,150)])
    number = StringField('Number', validators = [Length(0,100)])
    pages = StringField('Pages', validators = [Length(0,200)])
    keywords = StringField('Keywords', validators = [Length(0,250)])
    abstract = TextAreaField('Abstract', validators = [Length(0,2000)])
    notes = TextAreaField('Notes', validators = [Length(0,500)])
    primaryField = SelectField('Primary Field', validators = [Required()], choices = [('Philosophy/Ethics/Theology','Philosophy/Ethics/Theology'), ('Anthropology/Psychology/Sociology','Anthropology/Psychology/Sociology'), ('History/Politics/Law','History/Politics/Law'), ('Agriculture/Energy/Industry','Agriculture/Energy/Industry'), ('Animal Science/Welfare','Animal Science/Welfare'), ('Ecology/Conservation','Ecology/Conservation'), ('Nature Writing/Art/Literary Criticism','Nature Writing/Art/Literary Criticism'), ('Education/Living','Education/Living')])
    secondaryField = SelectField('Secondary Field', choices = [('','None'), ('Philosophy/Ethics/Theology','Philosophy/Ethics/Theology'), ('Anthropology/Psychology/Sociology','Anthropology/Psychology/Sociology'), ('History/Politics/Law','History/Politics/Law'), ('Agriculture/Energy/Industry','Agriculture/Energy/Industry'), ('Animal Science/Welfare','Animal Science/Welfare'), ('Ecology/Conservation','Ecology/Conservation'), ('Nature Writing/Art/Literary Criticism','Nature Writing/Art/Literary Criticism'), ('Education/Living','Education/Living')])
    link = StringField('Link', validators = [URL(), Optional()], filters = [lambda x: x or None])
    submit = SubmitField('Submit')

# Delete literature
# Not currently being used
class DeleteLitForm(Form):
    refType = SelectField('Reference Type', choices=[('Book Section','Book Section'), ('Edited Book', 'Edited Book') , ('Journal Article', 'Journal Article'), ('Journal Issue', 'Journal Issue'),
        ('Magazine Article', 'Magazine Article'), ('Media', 'Media'), ('Newspaper Article', 'Newspaper Article'), ('Report', 'Report'), ('Thesis', 'Thesis'), ('Website', 'Website')], default = None)
    title = StringField('Title', validators = [Required(), Length(1,150)])
    author = StringField('Author', validators = [Required(), Length(1,120)])
    submit = SubmitField('Delete Lit')
