############################
# URL rules
############################
from flask import render_template, make_response
from . import main
from .forms import SearchFormMain
from .. import db
# Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q
from ..decorators import admin_required
#######################
# Main Page #
#######################

@main.route('/', methods=['GET', 'POST'])
def index():

	# Create new main page search form
	form = SearchFormMain()

	# Get the number of objects in the "lit" collection of the db
	litcount = Lit.objects.count()

	# Render and return main page (index.html)
 	return render_template('index.html', form = form, litcount = litcount)

###############
# Information #
###############

@main.route('/about', methods=["GET"])
def about():
	return render_template('about.html')

@main.route('/history', methods=["GET"])
def history():
	return render_template('history.html')

@main.route('/manual', methods=['GET'])
def manual():
	return render_template('manAndInst.html')

