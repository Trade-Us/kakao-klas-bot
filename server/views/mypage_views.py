from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
bp = Blueprint('mypage', __name__, url_prefix='/mypage')

### MSI REVISE ###
from register import register_user
### MSI REVISE ###

@bp.route('/', methods=['POST'])
def mypage_home():
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



    