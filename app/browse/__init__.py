from flask import Blueprint

browse = Blueprint('browse', __name__, template_folder="templates")

from . import views