# Import the Form class, fields, and validators from wtform
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FieldList, IntegerField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Optional, Email, Regexp, NumberRange, URL
from wtforms import ValidationError
# Import database models
from ..models import User, Role

# Edit user profile
class EditProfileForm(Form):
    credentials = StringField('Credentials', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    description = TextAreaField('About me', validators=[Length(0, 1000)])
        #list_of_fields = ["Title", "Author", "Primary Field","Source Title", "Editor", "Year Published", "Type", "Creator", "Date Created", "Last Modified", "Last Modified By"]
        #fields = [(x, x) for x in list_of_fields]
        #searchFields = MultiCheckboxField('Search Table Fields', choices=fields)
    submit = SubmitField('Update')

# Admin profile
class EditProfileAdminForm(Form):
 	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
 	role = SelectField('Role')
 	name = StringField('Real name', validators=[Length(1, 64)])
 	location = StringField('Location', validators=[Length(0, 64)])
 	description = TextAreaField('About me', validators=[Length(0, 1000)])
 	confirmed = BooleanField('Confirmed')
 	approved = BooleanField('Approved')
 	activated = BooleanField('Activated')
        submit = SubmitField('Update')

 	def __init__(self, user, *args, **kwargs):
 		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
 		self.role.choices = [(role.name, role.name) for role in Role.objects()]
 		self.user = user

 	def validate_email(self, field):
 		if field.data != self.user.email and User.objects(email__iexact = field.data).first():
 			raise ValidationError('Email already registered.')

# Delete user
# Not currently being used
class DeleteUserForm(Form):
	email = EmailField("Email", validators=[Required()])
    	submit = SubmitField('Delete User')