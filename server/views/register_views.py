from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_

bp = Blueprint('register', __name__, url_prefix='/register')


@bp.route('/')
def notice_home():
    return 'Hello'

@bp.route('/signup', methods=['POST'])
def register_signup():
    content = request.get_json()
    print(content)
    content = content['action']
    content = content['params']
    parm_id = content['id']
    parm_password = content['password']
    print(parm_id,parm_password)
    dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : "공지사항",
                                    "description" : "test"
                                }
                            ]
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "messageText": "운영체제",
                        "action": "message",
                        "label": "운영체제"
                    },
                    {
                        "messageText": "알고리즘",
                        "action": "message",
                        "label": "알고리즘"
                    },
                    {
                        "messageText": "캡스톤",
                        "action": "message",
                        "label": "캡스톤"
                    },
                    {
                        "messageText": "데이터베이스",
                        "action": "message",
                        "label": "데이터베이스"
                    }
                ]
            }
        }
    return jsonify(dataSend)

@bp.route('/subject', methods=['POST'])
def register_subject():
    content = request.get_json()
    print(content)
    # content = content['action']
    # content = content['params']
    # parm_id = content['id']
    # parm_password = content['password']
    # print(parm_id,parm_password)
    dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : "공지사항",
                                    "description" : "test"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)