from flask import render_template, request, flash, session
from flask.ext.session import Session
from flask_paginate import Pagination
from . import search #calling on init py
from .forms import SearchForm
from .. import db # Import database model
from mongoengine.queryset.visitor import Q
from .searchForm import searchForm
from .functions import downloadResults
from .fuzzySearch import fuzzySearch
from .refineSearch import refineList

default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}


# Handles request for search page
@search.route('/search', methods=['GET', 'POST'])
def search():
	form = SearchForm()

	if request.method == 'POST':

		# If the request is to search
		if form.validate_on_submit():
			form, lit, total, preferences = searchForm(request, form)
			#session['search-post'] = form
			session['query'] = form.search.data
			session['lit'] = lit
			session['total'] = total
			session['preferences'] = preferences
			page = request.args.get('page', type=int, default=1)
			print('IN BASIC SEARCH with total entries ', session.get('total'))
			
		# If the request is from the main page
		elif request.form['submitBtn']=='main':
			form, lit, total, preferences =fuzzySearch(request)
			session['query'] = form.search.data
			session['lit'] = lit
			session['total'] = total
			session['preferences'] = preferences	
			page = request.args.get('page', type=int, default=1)
			print('IN FUZZY with total entries', session.get('total'))

		elif request.form['submitBtn']=='Export':
			return downloadResults(request.form)
			print('EXPORTING...')

	 	# If the request is to refine the list of search results
		elif request.form['submitBtn']=='RefineList':
			return refineList(request, "reg")
			session['query'] = form.search.data
			session['lit'] = lit
			session['preferences'] = preferences	
			print('REFINING LIST')

	send_lit=[]

	if request.method == 'GET': 
		print('inside GET request if statement ')
		if 'query' in session:
			form.search.data = session.get('query')
		if 'lit' in session:
			lit = session.get('lit')
		if 'total' in session:
			total = session.get('total')
		if 'preferences' in session:
			preferences = session.get('preferences')
		page = request.args.get('page', type=int, default=1)
	else: 
		page = 1

	#pagination
	print('beginning pagination total is ', total, " data", form.search.data)

	start = page*30-30
	end = page*30

	lastEntry = total

	temp = []

	if total>30 and (total-(page*30-30))>=end:
		for i in range(start, end):
			temp.append(lit[i])
		print(start, " and to ", end)
		print('if more than 30, length of what is left:', len(temp))

		send_lit.extend(temp)

	else:
		for i in range(start, lastEntry):
			temp.append(lit[i])
		print(start, " and to ", lastEntry+1)
		print('length of what is left:', len(temp))

		send_lit.extend(temp)

	pagination = Pagination(
		page=page, 
		per_page=30, 
		total=total, 
		record_name='references'
	)
	
	if total <= 0:
		flash("Your search returned nothing. Try other search terms.")
		return render_template('search.html', form = form, lit = lit, pagination = pagination, total = total, preferences = preferences )

		
	print('page number is', page, 'total is', total, 'size of lit', len(lit), 'size of send_lit', len(send_lit))
	# Otherwise return regular search page
	print('this is the regular search page we keep going into')
	return render_template('search.html', form = form, lit = send_lit, pagination = pagination, total = total, preferences = preferences )








