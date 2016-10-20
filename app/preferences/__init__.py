from flask import Blueprint

pref = Blueprint('pref', __name__, template_folder="templates")

from . import views