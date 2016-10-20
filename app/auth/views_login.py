##################################
# User login
##################################
from flask import render_template, redirect, request, url_for, flash
from . import auth #calls init file in auth
from ..models import User # Import database models
from .forms import LoginForm  #Import authentication forms defined in forms.py
from flask.ext.login import login_user, current_user, logout_user, login_required

# login url
# ie. If user accesses "obet.herokuap p.com/login" this method is called
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Create a new loginform
    form = LoginForm()
    # If the request made to this url has a valid form submission
    if form.validate_on_submit():
        # Search for the first email in the database that matches
        user = User.objects(email__iexact = form.email.data).first()
        # If the user exists then verify their password
        if user is not None and user.verify_password(form.password.data):
            # Set current user to be logged in
            login_user(user, form.remember_me.data)
            # Redirect the user to the index page
            return redirect(request.args.get('next') or url_for('main.index'))
        # Else display failed login message
        flash('Invalid username or password.')
    # Return login page with form
    return render_template('login.html', form = form)

# logout url
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    # Return main page
    return redirect(url_for('main.index'))

