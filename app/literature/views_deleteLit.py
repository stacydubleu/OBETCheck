from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash
from . import lit
from .forms import DeleteLitForm
from .. import db
# Import database model
from ..models import Lit, UserEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user

# Not currently in use ##############################################################

#################################
# Delete Lit Main Page Function #
#################################
from ..decorators import admin_required, permission_required, user_required
@lit.route('/deleteLit', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteLit():
 	form = DeleteLitForm()
 	if form.validate_on_submit():
		queryString = str(form.search.data)
 		lit = Lit.objects.search_text(queryString).order_by('$text_score')
		if len(lit) == 0:
 			flash("Your search returned nothing. Try other search terms.")
 		else:
 			return render_template('deleteLit.html', form = form, lit = lit)
 		return redirect(url_for('lit.deleteLit'))
 	return render_template('deleteLit.html', form = form)

##############################
# Delete Lit Helper Function #
##############################
@lit.route('/lit/<lit_id>/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteLiterature(lit_id):
	lit = Lit.objects( id__exact = lit_id).first()
	if lit is None:
		flash("No literature like this in the database.")
	else:
		userHist = UserEditRecord(litEdited = str(lit_id), litEditedTitle = lit.title, operation = "delete")
		current_user.update(push__u_edit_record=userHist)
		current_user.reload()
		lit.delete()
		flash("Literature has been deleted!")
	return redirect(url_for('search.search'))
