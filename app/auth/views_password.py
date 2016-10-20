##################################
# Password changes
##################################
from flask import render_template, redirect, request, url_for, flash
from . import auth #calls init file in auth
from ..models import User
# Import authentication forms defined in forms.py
from .forms import ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from ..email import send_email
from flask.ext.login import current_user, login_required

# Change password
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    # Create new change password form
    form = ChangePasswordForm()
    # If the request contains a submitted form
    if form.validate_on_submit():
        # Verify the password is not the same as the old
        if current_user.verify_password(form.old_password.data):
            # Save new password
            current_user.password = form.password.data
            current_user.save()
            #db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    # Else, if there is no form submission send "change password" page
    return render_template("change_password.html", form=form)

# Password reset request
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    # If the user is logged in, do not allow them to reset password
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    # Else create new password reset request form
    form = PasswordResetRequestForm()
    # If a form is submitted
    if form.validate_on_submit():
        # Retrieve user from db
        user = User.objects(email__iexact = form.email.data).first()
        # If the user exists
        if user:
            # Generate reset token
            token = user.generate_reset_token()
            # Send email to user to reset password
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        # Return user to login
        return redirect(url_for('auth.login'))
    # Else if a form is not submitted give reset password page
    return render_template('reset_password.html', form=form)

# Password reset
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    # If the user is logged in, do not allow them to reset password
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    # Create new Password reset form
    form = PasswordResetForm()
    # If form is submitted
    if form.validate_on_submit():
        user = User.objects(email__iexact=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        # If successfully reset password
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            # Redirect to login page
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('reset_password.html', form=form)
