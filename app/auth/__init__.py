from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder="templates")

from . import views_activate, views_admin, views_email
from . import views_login, views_password, views_registration