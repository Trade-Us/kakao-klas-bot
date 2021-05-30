from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
bp = Blueprint('logout', __name__, url_prefix='/logout')

### MSI REVISE ###
from register import register_user
### MSI REVISE ###

@bp.route('/', methods=['POST'])
def logout_home():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    user = User.query.filter_by(UserKey=kakaoid).first()
    if not user:
        dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                
                    "simpleText": {
                    
                        "text": "등록을 해지할 정보가 존재하지 않습니다."
                    
                    }
                
                }
            ]
        }
    }
        return dataSend
    db.session.delete(user)
    db.session.commit()
    db.session.close()

    dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                        
                        "description": "등록 해지가 성공적으로 완료되었습니다.\n 다시 로그인 하고 싶으시다면 로그인 버튼을 눌러주세요.",
                        "buttons": [
                            
                            {
                            "action":  "block",
                            "label": "로그인하기",
                            "blockId": "6072b7ac57f2de3814a5b3c1"
                            }
                        ]
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)
    



    