from flask import Blueprint, request

#from server import db
#from server.models import OnlineLecture

bp = Blueprint('onlinelecture', __name__, url_prefix='/onlinelecture')


@bp.route('/')
def onlinelecture_home():
    #1.유저 테이블에 아이디 비번 등록하고

    return 'Hello'

@bp.route('/list')
def onlinelecture_list():
    return 'Hello'