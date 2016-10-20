#################################
# Form definitions as classes
#################################

# Import the Form class, fields, and validators from wtform
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FieldList, IntegerField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Optional, Email, Regexp, NumberRange, URL
from wtforms import ValidationError
from wtforms import widgets
#from flask.ext.pagedown.fields import PageDownField

# Import database models
from ..models import User, Lit, Role

# Search form for index.html (main page)
class SearchFormMain(Form):
    # Search by
    search = StringField('Enter some terms to search on separated by a space:', validators = [Required()])
    # Submit button
    submit = SubmitField('Search')

# Test
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()