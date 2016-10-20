from flask import render_template
from . import lit
from .. import db
# Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q

#################
# Lit Main Page #
#################

# Display the literature
# lit_id in the url route is a variable, contains the literature's id
@lit.route('/lit/<lit_id>')
def lit(lit_id):

	# Retrieve the id
	lit = Lit.objects(id__iexact = lit_id).first()

	# If the lit does not exist send a 404 response
	if lit is None:
		abort(404)

	return render_template('lit.html', lit = lit)
