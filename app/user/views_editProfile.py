from flask import url_for, render_template, flash, redirect
from . import user
from .. import db
from .forms import EditProfileForm
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
################
# Edit Profile #
################

# Edit profile
@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()

	# On form submit, update profile information
 	if form.validate_on_submit():
 		current_user.update(set__name=form.name.data)
 		current_user.update(set__location=form.location.data)
 		current_user.update(set__credentials = form.credentials.data)
 		current_user.update(set__description = form.description.data)
 		flash('Your profile has been updated.')
 		return redirect(url_for('.user', email = current_user.email))

 	# If no submission, return form prefilled with current user profile information
 	form = EditProfileForm(None, current_user)
 	return render_template('editProfile.html', form=form)
