from flask_paginate import Pagination
from flask import render_template, redirect, url_for, flash, request, make_response
from .forms import SearchForm
from .. import db # Import database model
from ..models import Lit
from .functions import litToJson, convertId
from mongoengine.queryset.visitor import Q
import json

default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}

# Regular search
def searchForm(request, req_form):
 	form = SearchForm()
 	if req_form.search.data:
 		queryString = str(req_form.search.data)

 	lit = Lit.objects.search_text(queryString).order_by('$text_score')
 	total= lit.count();

	if len(lit) == 0:
  		return (form, None, 0, default_pref)

	else:
		# Sort lit ...check the 'sort by' drop down. if it is not blank do this
		if req_form.sort.data and str(req_form.sort.data) != 'None':
			sortStr = str(req_form.sort.data)
			lit = sorted(lit, key=lambda lit:getattr(lit, sortStr))

		
		# Convert lit to appropiate list object
		jsonlit = litToJson(lit)
		lit = json.loads(jsonlit)
		lit = convertId(lit)
		
		# Get 'preferences' cookie
		preferences = request.cookies.get('preferences')

		# If the cookie doesnt exist
		if not preferences:
			# Return default preferences
			preferences = default_pref

		else:
			# Otherwise convert the cookie to a python object
			preferences = json.loads(preferences)

		return ( 
			form,  
			lit, 
			total, 
			preferences
		)