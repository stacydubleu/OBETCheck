from flask import render_template
from . import user
from .. import db
from ..models import User
from mongoengine.queryset.visitor import Q

#####################
# User Profile Page #
#####################

# Display user's profile
# name in the url route is a variable that contains the user's name
@user.route('/user/<name>')
def user(name):

	# Retrieve user from db
	user = User.objects(name__iexact = name).first()

	# Sort and save the latest 5 changed the user has made
	latest_activity = user.u_edit_record
	latest_activity = sorted(latest_activity, key=lambda la: la.date, reverse=True)
	latest_activity = latest_activity[0:5]

	return render_template('user.html', user = user, latest_activity = latest_activity)
