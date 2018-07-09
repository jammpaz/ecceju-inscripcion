from flask import Blueprint

preventa = Blueprint('preventa', __name__)

from . import views
