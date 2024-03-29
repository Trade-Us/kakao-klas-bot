from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/', methods=['POST'])
def test():
    content = request.get_json()
    print(content)

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