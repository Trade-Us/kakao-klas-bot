from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_

bp = Blueprint('register', __name__, url_prefix='/register')

### MSI REVISE ###
from register import register_user
### MSI REVISE ###

@bp.route('/',methods=['POST'])
def register_home():
    content = request.get_json()
    # print(content)
    kakaoid = content['userRequest']['user']['id']
    
    content = content['action']
    content = content['params']
    parm_id = content['id']
    parm_password = content['password']
    name = "모상일"
    # print(parm_id,name,parm_password, kakaoid)
    ### MSI REVISE ###
    # 등록
    ## 해당 봇 key 가입 여부 확인
    ## 기등록자 여부 확인
    ## 로그인 정보 확인
    ## 듣는 과목 크롤링
    flag, data = register_user(parm_id,name, parm_password, kakaoid)
    if flag == -1:
        return data 
    ### MSI REVISE ###
    print(parm_id,parm_password)
    dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                        
                        "description": "등록이 성공적으로 완료되었습니다.\n\n메뉴를 선택해주세요",
                        "buttons": [
                            {
                            "action": "block",
                            "label": "내 현황 보기",
                            "blockId": "6082bcab51bb5918f598014e"
                            },
                            {
                            "action":  "block",
                            "label": "과목 별 확인",
                            "blockId": "6087e7fdc87b900e56c62ba6"
                            },
                            {
                            "action": "webLink",
                            "label": "광운대학교 홈페이지",
                            "webLinkUrl": "www.kw.ac.kr"
                            }
                        ]
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)

@bp.route('/signup', methods=['POST'])
def register_signup():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    
    content = content['action']
    content = content['params']
    parm_id = content['id']
    parm_password = content['password']
    name = "모상일"
    print(parm_id,name,parm_password, kakaoid)
    ### MSI REVISE ###
    # 등록
    ## 해당 봇 key 가입 여부 확인
    ## 기등록자 여부 확인
    ## 로그인 정보 확인
    ## 듣는 과목 크롤링
    flag, data = register_user(parm_id,name, parm_password, kakaoid)
    if flag == -1:
        return data 
    ### MSI REVISE ###
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
                                    "title" : "등록되셨습니다",
                                    "description" : "test"
                                }
                            ]
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "messageText": sub[0],
                        "action": "message",
                        "label": sub[0]
                    } for sub in data
                ]
            }
        }
    return jsonify(dataSend)

@bp.route('/subject', methods=['POST'])
def register_subject():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    
    content = content['action']
    content = content['params']
    parm_id = content['id']
    parm_password = content['password']
    name = "모상일"
    print(parm_id,name,parm_password, kakaoid)
    dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
        #   "title": "보물상자",
          "description": "등록이 성공적으로 완료되었습니다.\n\n메뉴를 선택해주세요",
          "buttons": [
            {
              "action": "message",
              "label": "내 현황 보기",
              "messageText": "아직 블록 연결 안함"
            },
            {
              "action":  "message",
              "label": "과목 별 확인",
              "messageText": "아직 블록 연결 안함"
            },
            {
              "action": "message",
              "label": "홈페이지 공지사항",
              "messageText": "아직 블록 연결 안함"
            },
          ]
        }
                    }
                ]
            }
        }
    return jsonify(dataSend)