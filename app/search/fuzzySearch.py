from flask import render_template, flash, request
from .forms import SearchForm
from .functions import litToJson, convertId
from .. import db # Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q
import json

##################
# Fuzzy Search
##################


# Default user preferences for search result fields display
default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}
  

def fuzzySearch(request):

	# Create new search form
 	form = SearchForm()

 	# Save information in request
 	req_form = request.form

 	# Save query made to return with the page so users can see the query they made previously
 	queryString = req_form['query']

 	# Set the search string in the new form to the old query
 	form.search.data = queryString

 	# If the user searched with an empty string simply return
 	if(queryString == ''):
		return (form, None, 0, default_pref)

	# Otherwise so a text search in the database
 	lit = Lit.objects.search_text(queryString).order_by('$text_score')

  	# If there were no results, return page
  	if len(lit) == 0:
		return (form, lit, 0, default_pref)

	# Otherwise return the page with the search results
	if len(lit) > 0:
		form.sort.data = ''

		total = lit.count()
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
		return (form, lit, total, preferences)