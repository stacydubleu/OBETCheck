from flask import url_for, render_template, flash, redirect
from . import user
from .. import db
from .forms import DeleteUserForm
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
from ..decorators import admin_required
from ..models import User

###############
# Delete User #
###############
## Does not work the way we want, yet.

@user.route('/deleteUser', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteUser():
 	form = DeleteUserForm()
 	if form.validate_on_submit():
		user = User.objects(email__iexact = form.email.data).first()
		if user is None:
 			flash("No user like this in the database.")
 		else:
 			user.delete()
 			flash("User Deleted.")
 		return redirect(url_for('user.deleteUser'))
 	return render_template('deleteUser.html', form = form)

