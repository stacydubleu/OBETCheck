######################
# Edit Preferences
######################
from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash, request, make_response
from . import pref
from .forms import Preferences
from .. import db
from mongoengine.queryset.visitor import Q
from flask.ext.login import current_user
import json

# Default user preferences for search result fields display
default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

@pref.route('/edit-pref', methods=['GET', 'POST'])
def preferences():
 	form = Preferences()

 	# If the user is logged in, take their preferences
	if current_user.is_authenticated():
		preferences = {"author": current_user.author, "yrPublished": current_user.yrPublished, "title":current_user.title, "sourceTitle": current_user.sourceTitle, "primaryField": current_user.primaryField, "creator": current_user.creator, "dateCreatedOn": current_user.dateCreatedOn, "editor": current_user.editor, "refType": current_user.refType, "lastModified": current_user.lastModified, "lastModifiedBy": current_user.lastModifiedBy}
 	else:
 		# Get cookie containing pref
 		preferences = request.cookies.get('preferences')
		if preferences:
			preferences = json.loads(preferences)

 	# If user does not have pref, give default
	if not preferences:
		preferences = default_pref

	# Debugging
	# print "GOT PREFERENCE"
	# for item in preferences:
	# 	print item + " "  + str(preferences[item])
	# print "END PREFERENCES FROM COOKIE"

	# If form is being submitted
 	if form.validate_on_submit():

 		# Create a dict from preferences in the form
 		for attr in form:
 			preferences[attr.name] = attr.data
		preferencesobj = Struct(**preferences)
 		form = Preferences(None, obj=preferencesobj)

 		# If user is logged in, save preferences to the db
 		if current_user.is_authenticated():
	 		current_user.update(set__title = form.title.data)
	 		current_user.update(set__author = form.author.data)
	 		current_user.update(set__primaryField = form.primaryField.data)
	 		current_user.update(set__editor = form.editor.data)
	 		current_user.update(set__yrPublished = form.yrPublished.data)
	 		current_user.update(set__refType = form.refType.data)
	 		current_user.update(set__creator = form.creator.data)
	 		current_user.update(set__dateCreatedOn = form.dateCreatedOn.data)
	 		current_user.update(set__lastModified = form.lastModified.data)
	 		current_user.update(set__lastModifiedBy = form.lastModifiedBy.data)
	 		flash('Your preferences have been saved')

	 	# Otherwise save their preferences to their browser as a cookie
 		else:
 			flash('Your preferences have been saved for your session')
			response = make_response(render_template('preferences.html', form=form))
	 		response.set_cookie('preferences', json.dumps(preferences))
			return response

 	# If no form is submitted, return the form prefilled with old preferences
	preferencesobj = Struct(**preferences)
 	form = Preferences(None, preferencesobj)
 	return render_template('preferences.html', form=form)
