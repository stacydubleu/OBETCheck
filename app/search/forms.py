#################################
# Form definitions as classes
#################################

# Import the Form class, fields, and validators from wtform
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required
from wtforms import ValidationError
from wtforms import widgets
#from flask.ext.pagedown.fields import PageDownField

# Search form for regular search
class SearchForm(Form):
	search = StringField('Enter some terms to search on separated by a space:', validators = [Required()])
        sort = SelectField('Sort by: ', choices = [('None',''), ('author', 'Author/Editor'), ('created_date', 'Date Created'), ('creator', 'Creator'), ('primaryField', 'Primary Field'), ('title', 'Title')])
        submit = SubmitField('Search')

# Not currently being used
# Advanced search
class AdvancedSearchForm(Form):
    	refType = SelectField('Reference Type', choices=[('Book Section','Book Section'), ('Edited Book', 'Edited Book') , ('Journal Article', 'Journal Article'), ('Journal Issue', 'Journal Issue'),
        ('Magazine Article', 'Magazine Article'), ('Media', 'Media'), ('Newspaper Article', 'Newspaper Article'), ('Report', 'Report'), ('Thesis', 'Thesis'), ('Website', 'Website')], default = None)
	title = StringField('Title', default = None)
	author = StringField('Author', default = None)
    	submit = SubmitField('Search')