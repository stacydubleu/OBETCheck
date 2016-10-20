from flask import render_template, redirect, url_for, flash, request, make_response
from . import search
from .. import db
# Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q
from .refineSearch import refineList
from .functions import litToJson, convertId
import json, cgi

###################
# Advanced Search
###################

# Utility functions to escape strange characters
def convertCat(category):
	convertedString = ''
	# validate the string, excape all special chars
	# ...?
	convertedString = cgi.escape(category, quote=True)
	return convertedString

def convertCont(contains):
	convertedString = ''
	# validate
	# ...
	convertedString = cgi.escape(contains, quote=True)
	return convertedString

def convertInp(inputtext):
	convertedString = ''
	convertedString = cgi.escape(inputtext, quote=True)
	print convertedString
	return convertedString

def convertCond(condition):
	convertedString = ''
	if(condition == "and"):
		return "&"
	elif(condition == "not"):
		return "ne"
	else:
		return "|"

# Returns if the text is valid or not
def validInputText(inputtext):
	# Need to escape special characters
	inputtext = inputtext.strip()
	if(inputtext=="" or inputtext==None):
		return False
	else:
		return True

# Utility function to create a query segment from advanced search form
# first is a boolean that says whether the current segment is the first segment in their query
def createQuerySeg(x, first):
	querySeg = ""
	negation = ""
	# # Name of each input field
	# category = 'category1'
	# contains = 'contains1'
	# inputtext = 'inputtext1'
	# condition = 'condition1'

	# Name of each input field
	categoryx = 'category' + str(x)
	containsx = 'contains' + str(x)
	inputtextx = 'inputtext' + str(x)
	conditionx = 'condition' + str(x)
	# Get values from submitted form
	categorystring = request.form[categoryx]
	containsCond = request.form[containsx]
	inputtext = request.form[inputtextx]
	condition = request.form[conditionx]
	# Filter the condition (not, and, or)
	convertedCond = convertCond(condition)
	# Convert the condition to query language
	if(convertedCond=="ne"):
		negation = "__not"
		if(not first):
			querySeg += "&"
	elif(not first):
		querySeg += convertedCond

	if (validInputText(inputtext)):
		inputtext = convertInp(inputtext)
		containsCond = convertInp(containsCond)
		categorystring = convertCat(categorystring)
		# Take the values and convert to model atribute names
		if(categorystring == 'KeywordsAbstractNotes'):
			querySeg += ('(Q(keywords' + negation + '__icontains ="' + inputtext + '") | Q(abstract' +
				negation + '__icontains ="' + inputtext + '") | Q(notes' + negation + '__icontains ="' + inputtext + '"))')
		elif(categorystring == 'PrimarySecondary'):
			querySeg += ('(Q(primaryField' + negation + '__' + containsCond + ' ="' + inputtext +
				'") | Q(secondaryField' + negation + '__' + containsCond + ' ="' + inputtext + '"))')
		elif(categorystring == 'CreatedBy'):
			querySeg += ('Q(creator' + negation + '__' + containsCond + ' ="' + inputtext + '")')
		elif(categorystring == 'ModifiedBy'):
			querySeg += ('Q(last_edit__lastUserEdited' + negation + '__' + containsCond + ' ="' + inputtext + '")')
		# else if for DATE - needs to be done
		elif(categorystring == 'DateCreated'):
			querySeg += ('Q()')
		else:
			querySeg += ("Q(" + categorystring + negation + "__" +
			containsCond + " ='" + inputtext + "')")
	return querySeg

# Handler for advanced search url request
@search.route('/advancedSearch', methods=['GET', 'POST'])
def advancedSearch():
	default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}
	# If the request made is a POST request
	if request.method == 'POST':
		try:
			# If the button "RefineList" was the one that sent the request
			if(request.form['submitBtn']=='RefineList'):
				# Call refineList
				return refineList(request, "adv")
			# If the request was from "Export" button
			elif request.form['submitBtn']=='Export':
				# Call downloadResults
				return downloadResults(request.form)
		except:
			# Get 'preferences' cookie
			preferences = request.cookies.get('preferences')
			# If the cookie doesnt exist
			if not preferences:
				# Return default preferences
				preferences = default_pref
			else:
				# Otherwise convert the cookie to a python object
				preferences = json.loads(preferences)
			cond = 'condition1'
			first = True
			# get number of conditions
			count = int(request.form['count'])
			# string to contain the mongo query
			query = 'lit = Lit.objects('
			# go through all the conditions and add the information to
			for x in xrange(1, count+1):
				condx = str.replace(cond, '1', str(x))
				# check if the condition is ignore
				if( request.form[condx] != 'ignore' ):
					print "checking for ignore"
					# if not ignore then add the information to the mongo query
					# get the information from the 4 input fields
					temp = createQuerySeg(x, first)
					if(temp != None and temp != ''):
						query += temp
						first = False
			query += (')')
			print "query is :" + query
			if( len(query) != 19 ):
				# Execute query
				exec query
				# print json.dumps(lit)
				# lit = Lit.objects(Q(author__iexact = 'bob') | Q(keywords__icontains = 'only'))
				# print json.dumps(lit)
				if( len(lit) != 0 ):
					# Convert lit to appropiate list object
					jsonlit = litToJson(lit)
					lit = json.loads(jsonlit)
					lit = convertId(lit)
					sessioninfo = json.dumps(request.form)
					# Render advanced search page
					return render_template('advancedSearch.html', lit = lit, sessioninfo = sessioninfo, preferences = preferences)
				# Otherwise there were no results
				else:
					flash("Your query had no results.")
					sessioninfo = json.dumps(request.form)
					return render_template('advancedSearch.html', sessioninfo = sessioninfo, preferences = preferences)

 	return render_template('advancedSearch.html')
