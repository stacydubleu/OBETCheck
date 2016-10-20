from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash
from . import lit
from .forms import AddLitForm
from .. import db
# Import database model
from ..models import Lit, LitEditRecord, UserEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
###########
# Add Lit #
###########

# Add literature
@lit.route('/addLit', methods=['GET', 'POST'])
@login_required
def addLit():

	# Create new add lit form
 	form = AddLitForm()

 	# On form submission
 	if form.validate_on_submit():

 		# If the literature is already in the database, then do not add the material, return
		lit = Lit.objects(title__iexact = form.title.data, author__iexact = form.author.data, pages__iexact = form.pages.data).first()
		if lit is not None:
 			flash("This is already in the DB. This is the page")
			return render_template('lit.html', lit = lit)

		# Create a new lit object, save to db first, then update fields
		lit = Lit(refType = form.refType.data, title = form.title.data, author = form.author.data, primaryField = form.primaryField.data, creator = current_user.name)
		lit.save()
		lit.update(set__yrPublished = form.yrPublished.data)
		lit.update(set__sourceTitle = form.sourceTitle.data)
		lit.update(set__editor = form.editor.data)
		lit.update(set__placePublished = form.placePublished.data)
		lit.update(set__publisher = form.publisher.data)
		lit.update(set__volume = form.volume.data)
		lit.update(set__number = form.number.data)
		lit.update(set__pages = form.pages.data)
		lit.update(set__abstract = form.abstract.data)
		lit.update(set__notes = form.notes.data)
		lit.update(set__secondaryField = form.secondaryField.data)

		# Add user's edit in edit history
		editHist = LitEditRecord(lastUserEdited = current_user.name)

		# If the link field is not empty, save the link too
		# If statement is done because update fails when attempting to save an empty string
		if form.link.data is not None:
			lit.update(set__link = form.link.data)

		# Add keywords into the db as a listField
		keywordslist = (form.keywords.data).split(",")
		for x in range(0, len(keywordslist)):
			key = str(keywordslist[x].strip())
			lit.update(push__keywords = key)

		# Update lit history
		lit.update(push__l_edit_record=editHist)
		lit.update(set__last_edit = editHist)
		lit.reload()

		# Update user edit history
		userHist = UserEditRecord(litEdited = str(lit.id), operation = "add", litEditedTitle = lit.title)
		current_user.update(push__u_edit_record = userHist)
		current_user.reload()

		flash("Successfully added!")
 		return redirect(url_for('lit.lit', lit_id = lit.id))
 	return render_template('addLit.html', form = form)
