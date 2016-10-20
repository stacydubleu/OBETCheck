# Import the Form class, fields, and validators from wtform
from flask.ext.wtf import Form
from wtforms import BooleanField, SubmitField

# User preferences for search results view
# User may chose which fields to show in their search results
class Preferences(Form):
    author = BooleanField('Author')
    yrPublished = BooleanField('Year Published')
    title = BooleanField('Title')
    sourceTitle = BooleanField('Source Title')
    primaryField = BooleanField('Primary Field')
    editor = BooleanField('Editor')
    refType = BooleanField('Reference Type')
    creator = BooleanField('Creator')
    dateCreatedOn = BooleanField('Date Created')
    lastModified = BooleanField('Last Modified')
    lastModifiedBy = BooleanField('Last Modified By')
    submit = SubmitField('Update')