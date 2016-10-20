from flask import render_template, redirect, url_for, flash, request, make_response
from .forms import SearchForm
from .. import db # Import database model
from ..models import Lit
from .functions import litToJson, convertId
from mongoengine.queryset.visitor import Q
import json

# Regular search
def searchForm(request, req_form):
 	form = SearchForm()
 	if req_form.search.data:
 		queryString = str(req_form.search.data)

 	lit = Lit.objects.search_text(queryString).order_by('$text_score')

 	if len(lit) == 0:
 		flash("Your search returned nothing. Try other search terms.")
		return render_template('search.html', form = form, lit = lit)

	else:
		# Sort lit
		if req_form.sort.data and str(req_form.sort.data) != 'None':
			sortStr = str(req_form.sort.data)
			lit = sorted(lit, key=lambda lit:getattr(lit, sortStr))

		# Convert lit to appropiate list object
		jsonlit = litToJson(lit)
		lit = json.loads(jsonlit)
		lit = convertId(lit)
		default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}
		# Get 'preferences' cookie
		preferences = request.cookies.get('preferences')

		# If the cookie doesnt exist
		if not preferences:
			# Return default preferences
			preferences = default_pref

		else:
			# Otherwise convert the cookie to a python object
			preferences = json.loads(preferences)

		return render_template('search.html', form = form, lit = lit, preferences = preferences)