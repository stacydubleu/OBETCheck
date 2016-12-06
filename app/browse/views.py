##########
# Browse #
##########
from flask_paginate import Pagination
from flask import render_template, redirect, url_for, flash, request, make_response
from . import browse
from .. import db
# Import database model
from ..models import Lit, LitEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
import json

# Default user preferences for search result fields display
default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}
  

@browse.route('/browse', methods = ['GET'])
def browse():

	search = False
	q = request.args.get('q')
	if q:
		search = True
	
	total = Lit.objects.count()
	page = request.args.get('page', type=int, default=1)

	start=page*30-30
	end=page*30
	lit = Lit.objects[start:end].order_by('-create_date')
	pagination = Pagination(
		page=page, 
		per_page=30, 
		total=total, 
		search=search, 
		record_name='references'
	)

	preferences = request.cookies.get('preferences')
	if not preferences:
 		# Return default preferences
 		preferences = default_pref
 	else:
 		# Otherwise convert the cookie to a python object
 		preferences = json.loads(preferences)

	return render_template(
		'browse.html',
    	lit = lit,
    	pagination = pagination,
    	total=total,
    	preferences = preferences,
    	)