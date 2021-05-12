from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/login', methods=['POST'])
def notice_keyword():
    content = request.get_json()
    print(content)
    content = content['action']
    content = content['params']
    keyword = content['키워드']
    name = content['이름']

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
                                "description" : notice_name
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)