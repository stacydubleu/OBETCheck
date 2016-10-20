##########
# Browse #
##########
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash, request, make_response
from . import browse
from .. import db
# Import database model
from ..models import Lit, LitEditRecord, Pagination
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
import json

PER_PAGE=20

@browse.route('/browse', defaults={'page': 1}, methods=['GET'])
@browse.route('/browse/page/<int:page>')
def browse(page):
	count= 20;
	lit= Lit.objects[:50].order_by('-created_date')
	if not lit and page !=1:
		abort(404)
	pagination = Pagination(page, PER_PAGE, count)
	# Retrieve the first 50 lit objects from the db
	# Get 'preferences' cookie
	preferences = request.cookies.get('preferences')

	# If the cookie doesnt exist
	if not preferences:

		# Return default preferences
		preferences = default_pref

	else:

		# Otherwise convert the cookie to a python object
		preferences = json.loads(preferences)

	# Render template with the list of literature and preferences obj and send to client
	return render_template('browse.html', pagination=pagination, lit=lit, preferences=preferences)
