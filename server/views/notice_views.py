from flask import Blueprint, request

#from server import db
#from server.models import Notice

bp = Blueprint('notice', __name__, url_prefix='/notice')


@bp.route('/')
def notice_home():
    return 'Hello'

@bp.route('/list')
def notice_list():
    return 'Hello'