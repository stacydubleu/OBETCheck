##################################
# Registration-related views
##################################
from flask import render_template, redirect, request, url_for, flash, current_app
from . import auth #calls init file in auth
from ..models import User
from .forms import RegistrationForm
from ..email import send_email
from flask.ext.login import current_user, login_required

# Registration for users
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Create registration form
    form = RegistrationForm()
    # If the form is submitted and valid
    if form.validate_on_submit():
        # Create a new user
        user = User()
        # Set the attributes of the new user to form inputs
        user.email = form.email.data
        user.name = form.name.data
        user.password = form.password.data
        # Save the user to the database
        user.save()
        # Save form information as name, email, reason
        name = form.name.data
        email = form.email.data
        print(email);
        reason = form.reason.data
        # If the email matches the current admin's email then automatically approve
        if form.email.data == current_app.config['OBET_ADMIN']:
            flash('Welcome to OBET, new Admin! Please log in to continue.')
            user.approve()
            # Return login page
            return redirect(url_for('auth.login'))
        # Else, send an email to the admin, template found in "auth/email/adminConfirmation"
        send_email(current_app.config['OBET_ADMIN'], 'New User Information', 'auth/email/adminConfirmation', name = name, email = email, reason = reason)
        flash('The admin must approve your registration before you will be able to register. Check your email soon.')
        #token = user.generate_confirmation_token()
        #send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        #flash('A confirmation email has been sent to you by email.')
        # Redirect user to main page
        return redirect(url_for('main.index'))
    # If no form is submitted, return registration page
    return render_template('register.html', form = form)

# Confirm email
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    # Confirm user if not already
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    # Send main page
    return redirect(url_for('main.index'))

# Such a function is executed before each request, even if outside of a blueprint.
#   - flask docs
@auth.before_app_request
def before_request():
    # If user is not authenticated redirect them to "unconfirmed" page,
    # otherwise continue with their request
    if current_user.is_authenticated() and not current_user.confirmed and request.endpoint[:5] != 'auth.':
        #print "Before request function not working for some reason."
        return redirect(url_for('auth.unconfirmed'))
    #if current_user.is_authenticated() and not current_user.activated and request.endpoint[:5] != 'auth.':
    #   return redirect(url_for('auth.deactivated'))

# Unconfirmed
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect('main.index')
    return render_template('unconfirmed.html')

# Resent confirmation
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user = current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

