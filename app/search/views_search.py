from flask import render_template, request
from . import search #calling on init py
from .forms import SearchForm
from .. import db # Import database model
from mongoengine.queryset.visitor import Q
from .searchForm import searchForm
from .functions import downloadResults
from .fuzzySearch import fuzzySearch
from .refineSearch import refineList

# Handles request for search page
@search.route('/search', methods=['GET', 'POST'])
def search():
 form = SearchForm()
 if request.method == 'POST':

	 # If the request is to search
	 if form.validate_on_submit():
	 	return searchForm(request, form)

	 # If the request is from the main page
	 elif request.form['submitBtn']=='main':
	 	return fuzzySearch(request)
	 elif request.form['submitBtn']=='Export':
	 	return downloadResults(request.form)

 	 # If the request is to refine the list of search results
	 elif request.form['submitBtn']=='RefineList':
		return refineList(request, "reg")

 # Otherwise return regular search page
 return render_template('search.html', form = form)
