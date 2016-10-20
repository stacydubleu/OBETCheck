from flask import Blueprint

search = Blueprint('search', __name__, template_folder="templates")

from . import views_advancedSearch, views_search