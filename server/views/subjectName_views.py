from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_

bp = Blueprint('subjectName', __name__, url_prefix='/subjectName')

### MSI REVISE ###
from register import register_user
### MSI REVISE ###

@bp.route('/', methods=['POST'])
def subjectName_home():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    
    content = content['action']
    content = content['params']
    parm_subjectName = content['subjectName']

    user_list = User.query.filter_by(UserKey=kakaoid)
    for user in user_list:
        print(user.ID)
        user_id = user.ID
    
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    
    if parm_subjectName in usersubject_list:
        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                            
                            "description": f"{parm_subjectName}\n\n공지사항",
                            "buttons": [
                                {
                                "action": "message",
                                "label": "최근 공지 보기",
                                "messageText": "아직 블록 연결 안함"
                                },
                                {
                                "action":  "message",
                                "label": "키워드 검색",
                                "messageText": "아직 블록 연결 안함"
                                }
                            ]
                            }
                        }, #for i in range(3)
                        {
                            "basicCard": {
                            
                            "description": f"{parm_subjectName}\n\n과제",
                            "buttons": [
                                {
                                "action": "message",
                                "label": "진행 중인 과제",
                                "messageText": "아직 블록 연결 안함"
                                },
                                {
                                "action":  "message",
                                "label": "미제출 과제",
                                "messageText": "아직 블록 연결 안함"
                                }
                            ]
                            }
                        },
                        {
                            "basicCard": {
                            
                            "description": f"{parm_subjectName}\n\n온라인 강의",
                            "buttons": [
                                {
                                "action": "message",
                                "label": "진행 중인 강의",
                                "messageText": "아직 블록 연결 안함"
                                },
                                {
                                "action":  "message",
                                "label": "미시청 강의",
                                "messageText": "아직 블록 연결 안함"
                                }
                            ]
                            }
                        }

                    ]
                }
            }
        return jsonify(dataSend)
    else:
        des=""
        for sub in usersubject_list:
            des+=sub
            des+="\n\n"

        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                            
                            "description": f"이 중 하나를 정확하게 입력해주세요.\n\n{des}",
                            "buttons": [
                                {
                                "action": "message",
                                "label": "다시 입력",
                                "messageText": "아직 블록 연결 안함"
                                }
                            ]
                            }
                        } #for subjectN in usersubject_list                      
                    ]
                }
            }
        return jsonify(dataSend)

@bp.route('/notice_recent', methods=['POST'])
def subjectName_notice_recent():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    
    content = content['action']
    content = content['params']
    parm_subjectName = content['subjectName']
    
    user = User.query.filter_by(UserKey=kakaoid).first()

    if not user:
        return -1
    user_id = user.ID
    
    subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    #subject_list = IDWithSubject.query.filter_by(SubjectID=subject_id).all()
    print("\nlog:",subject_id)
    notice_list = Notice.query.filter(or_(
        Notice.SubjectID == f"{subject_id}"
        
        )
    ).order_by(Notice.Date.desc())[:5]

    notice_name = []
    for notice in notice_list:
        subject_name = Subject.query.filter_by(ID=notice.SubjectID).first().Name

        notice_name.append([subject_name,notice.Title,notice.Contents])
    
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                    
                        "text": f"{notice[1]}\n\n{notice[2]}",
                    
                    }
                } for notice in notice_name                

            ]
        }
    }

    return jsonify(dataSend)

@bp.route('/notice_keyword', methods=['POST'])
def subjectName_notice_keyword():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    
    content = content['action']
    content = content['params']
    parm_subjectName = content['subjectName']
    parm_keyword = content['keyword']
    
    user = User.query.filter_by(UserKey=kakaoid).first()

    if not user:
        return -1
    user_id = user.ID
    
    subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID

    notice_list = Notice.query.filter_by(SubjectID=subject_id)
    for notice in notice_list:
        print(notice)      
        if parm_keyword in notice.Title:
            notice_name = []
            subject_name = Subject.query.filter_by(ID=notice.SubjectID).first().Name
            notice_name.append([subject_name,notice.Title,notice.Contents])

    
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                    
                        "text": f"{notice[1]}\n\n{notice[2]}",
                    
                    }
                } for notice in notice_name                

            ]
        }
    }

    return jsonify(dataSend)

@bp.route('/subject', methods=['POST'])
def register_subject():
    content = request.get_json()
    print(content)
    kakaoid = content['userRequest']['user']['id']
    
    
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