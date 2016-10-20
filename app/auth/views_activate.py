##################################
# User activation/deactivation
##################################
from flask import render_template, redirect, request, url_for, flash
from . import auth #calls init file in auth
from flask.ext.login import current_user, login_required

# Activate user
@auth.route('/activate')
@login_required
def activate():
    if current_user.activated:
        flash('Already activated. Welcome back!')
        return redirect(url_for('main.index'))
    current_user.activate()
    flash('Account reactivated! Welcome back!')
    return render_template('main.index')

# Deactivate account
@auth.route('/deactivate')
@login_required
def deactivate():
    if current_user.activated:
        flash('Account already deactivated.')
        return redirect(url_for('main.index'))
    current_user.deactivate()
    flash('Account deactivated! We\'ll miss you!')
    return render_template('main.index')

# Already deactivated account
@auth.route('/deactivated')
def deactivated():
    if current_user.is_anonymous() or current_user.activated:
        return redirect('main.index')
    return render_template('deactivated.html')