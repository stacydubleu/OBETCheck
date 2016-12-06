from flask import Blueprint
from flask_paginate import Pagination

browse = Blueprint('browse', __name__, template_folder="templates")

from . import views
