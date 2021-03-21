from flask import Blueprint, request

#from server import db
#from server.models import Assignment

bp = Blueprint('assignment', __name__, url_prefix='/assignment')


@bp.route('/')
def assignment_home():
    return 'Hello'

@bp.route('/deadline')
def assignment_deadline():
    return 'Hello'

