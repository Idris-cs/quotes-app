from flask import Blueprint

main = Blueprint('main', __name__)

# Import routes AFTER blueprint is created to avoid circular imports
from . import routes  # noqa
