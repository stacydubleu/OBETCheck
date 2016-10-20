from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash, request, make_response
from .. import db # Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q
import json, cgi, csv, io, collections

# Utility function
def litToJson(lit):
	# Create a json string of lit
	jsonlit = '['
	for literature in iter(lit):
		jsonlit+= ( literature.to_json() + ", ")
	# Remove the last comma and space
	if len(jsonlit) > 7:
		jsonlit = jsonlit[:-2]
	jsonlit += "]"
	return jsonlit

# Utility function to convert lit object into string
def convertId(lit):
	for l in lit:
		# Convert id to basic string id
		litid = "%s" % l["_id"]
		litid = litid.replace("{u'$oid': u'", "")
		litid = litid.replace("'}", "")
		l["id"] = litid

		# Convert date to basic date
		litdate = "%s" % l["created_date"]
		litdate = litdate.replace("{u'$date': ", "")
		litdate = litdate.replace("L", "")
		litdate = int(litdate.replace("}", ""))
		litdate = litdate/1000.0
		litdate = str(datetime.fromtimestamp(litdate).strftime('%Y-%m-%d %H:%M:%S'))
		l["created_date"] = litdate

		# Convert date to basic date
		if("last_edit" in l.keys()):
			litdate = "%s" % l["last_edit"]["date"]
			litdate = litdate.replace("{u'$date': ", "")
			litdate = litdate.replace("L", "")
			litdate = int(litdate.replace("}", ""))
			litdate = litdate/1000.0
			litdate = str(datetime.fromtimestamp(litdate).strftime('%Y-%m-%d %H:%M:%S'))
			l["last_edit"]["date"] = litdate

	return lit

# Utility function to
# append creator name to the literature object being returned to the template
def appendCreatorName(lit):
	for l in lit:
		l["creator_name"] = lit

# Request coming from the main page
# Return the template for regular search

########################
# Export to CSV
########################

# Utility function to delete specified keys
#  *keys is any number of arguments after it
# it is the dict item
def dict_filter(it, *keys):
    for item in it:
	    for k in keys:
	    	del item[k]

# Recursively encode items in dict to utf-8
def encode(data):
    if isinstance(data, basestring):
        return data.encode('utf8', 'ignore')
    elif isinstance(data, collections.Mapping):
        return dict(map(encode, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(encode, data))
    else:
        return data

# This route will prompt a file download with the csv lines
def downloadResults(request_form):
	# Get search results they want to export
	formString = request_form['redefinedString']

	# Convert to python object
	search_results = json.loads(formString)

	# Get list of id's from the redefined string
	id_list = []
	for item in search_results:
		id_list.append(item["id"])

	# Query the database for those lit
	lit = Lit.objects(id__in=id_list)

	# Create a json from that result
	lit = litToJson(lit)
	lit = json.loads(lit)

	# Remove unnecessary fields
	header = sorted(["abstract","author","editor","keywords","link","notes","number","pages","placePublished","primaryField","publisher","refType","secondaryField","sourceTitle","title","volume","yrPublished","DOI"])
	dict_filter(lit, "_id", "l_edit_record", "last_edit", "created_date", "creator")
	header = encode(header)

	# Transfrom it into a tsv with DictWriter
	sio = io.BytesIO()
	dw = csv.DictWriter(sio, header, delimiter='\t')
	dw.writeheader()
	for l in lit:
		l = encode(l)
		dw.writerow(l)

    # We need to modify the response, so the first thing we
    # need to do is create a response out of the CSV string
	response = make_response(sio.getvalue())

    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
	response.headers["Content-Disposition"] = "attachment; filename=obet_search.tsv"
	return response
