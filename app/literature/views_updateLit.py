from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, flash
from . import lit
from .forms import AddLitForm
from .. import db
# Import database model
from ..models import User, Lit, LitEditRecord, UserEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user

##############
# Update Lit #
##############

# Update literature
@lit.route('/updateLit/<lit_id>', methods=['GET','POST'])
@login_required
def updateLit(lit_id):

	# Get lit object by id
	lit = Lit.objects(id__iexact = lit_id).first()

	# Create new add lit form ( also used as an update lit form )
	form = AddLitForm(None, lit)

	# Join the keywords into a string and set the form to contain this
	keywordslist = ', '.join(lit.keywords).encode('utf-8')
	form.keywords.data = keywordslist

	# Return the update page
	return render_template('update.html', form = form, lit = lit)

#################
# Submit Update #
#################

# When user submits the update lit form ( Could be combined with the updateLit method )
@lit.route('/updateLitSub/<lit_id>', methods=['POST'])
@login_required
def updateLitSub(lit_id):
	form = AddLitForm()
	lit = Lit.objects(id__iexact = lit_id).first()

	# Update all the fields of the object ( Could possibly be done in a simpler fashion )
	if form.validate_on_submit():
		lit.update(set__title=form.title.data)
		lit.update(set__refType=form.refType.data)
		lit.update(set__author=form.author.data)
		lit.update(set__primaryField=form.primaryField.data)
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
		lit.update(set__secondaryField= form.secondaryField.data)
		lit.update(set__link = form.link.data)

		# Clear the objects keywords
		lit.update(set__keywords = [])

		# Separate the keywords field string by comma
		keywordslist = (form.keywords.data).split(",")

		# Push each key into the obj list field
		for x in range(0, len(keywordslist)):
			key = str(keywordslist[x].strip())
			if key is not None :
				lit.update(push__keywords = key)

		# Add new Lit history obj
		editHist = LitEditRecord(lastUserEdited = current_user.name)
		lit.update(push__l_edit_record=editHist)
		lit.update(set__last_edit = editHist)
		lit.reload()

		# Add new User edit history obj
		userHist = UserEditRecord(litEdited = str(lit.id), operation = "update", litEditedTitle = lit.title)
		current_user.update(push__u_edit_record=userHist)
		current_user.reload()

		lit = Lit.objects(id__iexact = lit_id).first()
		flash(lit.title + " has been updated")
	else:
		flash(lit.title + " failed to be updated")
	return render_template('lit.html', lit = lit)
