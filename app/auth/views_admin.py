#####################################
# URL rules related to admin responsibilities
#####################################

# Import flask modules
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user
from . import auth #calls init file in auth
# Import database models
from ..models import User, Role, Lit
# Import authentication forms defined in forms.py
from .forms import LoginForm, RegistrationForm, ReasonForm, ChangePasswordForm
from .forms import PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..email import send_email
from flask import current_app
from flask.ext.login import current_user, logout_user, login_required
from ..decorators import admin_required
# Approve user, Admin approve user's application
@auth.route('/approveUser/<email>', methods=['GET', 'POST'])
@login_required
@admin_required
def approveUser(email):
    # Retrieve the the user (by email) from db
    user = User.objects(email__iexact = email).first()

    # If the user does not exist
    if user is None:
        # Redirect to main page with message
        flash('That user is no longer in the database to approve.')
        return redirect(url_for('main.index'))

    # If user is already confirmed, return to main page with message
    if user.confirmed:
        flash('This user has already been approved.')
        return redirect(url_for('main.index'))

    # Call generate_confirmation_token on User obj
    token = user.generate_confirmation_token()

    # Send email to user
    send_email(user.email, 'You\'ve been accepted to join OBET! Please confirm your account.', 'auth/email/confirm', user = user, token = token)
    flash('The user has been emailed their confirmation information.')

    # Approve user
    user.approve()

    # return to main page
    return redirect(url_for('main.index'))

# Reject user, done by admin
@auth.route('/rejectUser/<email>', methods=['GET', 'POST'])
@login_required
@admin_required
def rejectUser(email):
    # Retrieve user from db
    user = User.objects(email__iexact = email).first()
    if user.confirmed:
            flash('This user has already been approved. Delete their account if you would like to remove them.')
            return redirect(url_for('main.index'))
    if user is None:
        flash('That user is no longer in the database to approve.')
        return redirect(url_for('main.index'))
    form = ReasonForm()
    # If form submitted to reject usre
    if form.validate_on_submit():
        reason = form.reason.data
        admin = current_user
        # Send email to user on their rejection
        send_email(user.email, 'Your OBET User Status', 'auth/email/rejectNotice', user = user, reason = reason, admin = admin)
        flash('The user has been emailed their rejection.')
        # Delete user
        user.delete()
        # Return admin to main page
        return redirect(url_for('main.index'))
    # Else send "reject user" page
    return render_template('rejectUser.html', form = form)

