from flask import Blueprint

lit = Blueprint('lit', __name__, template_folder="templates")

from . import views_addLit, views_deleteLit, views_lit, views_updateLit