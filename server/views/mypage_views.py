from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture,NewUser
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
    kakaoid = content['userRequest']['user']['id']
    user = User.query.filter_by(UserKey=kakaoid).first()
    if not user:
        nuser = NewUser.query.filter_by(UserKey=kakaoid).first()
        if not nuser:
            dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                            
                            "description": "등록되지 않은 사용자입니다. ID등록 후 이용해주시기 바랍니다.",
                            "buttons": [
                                {
                                "action": "block",
                                "label": "등록하기",
                                "blockId": "6072b7ac57f2de3814a5b3c1"
                                }
                            ]
                            }
                        } #for subjectN in usersubject_list                      
                    ]
                }
            }
        else:
            dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                    
                        "simpleText": {
                        
                            "text": "등록이 진행중입니다. 잠시만 기다려주세요"
                        
                        }
                    
                    }
                ]
            }
            }
        return dataSend
    user_id = user.ID

    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    mypage_list = []
    text = ""
    for subject in subject_list:
        assignCount = 0
        onlineCount = 0
        onlinestr = "\n\n\n강의"
        assignstr = "\n\n\n과제"
        assignment_list = Assignment.query.filter_by(UserID=user_id,SubjectID=subject.SubjectID)
        for assignment in assignment_list:      
            if assignment.StartDate <= datetime.now() and assignment.EndDate >= datetime.now():
                if assignment.Submit == True:
                    state = "제출"
                else:
                    state = "미제출"
                assignCount += 1
                assignstr += f"\n\n{str(assignCount)}. {assignment.Title} : {state}\n마감날짜:{assignment.EndDate}"               
        online_list = OnlineLecture.query.filter_by(UserID=user_id,SubjectID=subject.SubjectID)
        for online in online_list:
            if online.StartDate <= datetime.now() and online.EndDate >= datetime.now():
                onlineCount += 1
                onlinestr += f"\n\n{str(onlineCount)}. {online.Contents} : {online.Progress}\n마감날짜:{online.EndDate}"
        print(subject.SubjectID,assignCount,onlineCount)
        if assignCount > 0 or onlineCount >0:
            #mypage_list.append([Subject.query.filter_by(ID=subject.SubjectID).first().Name,onlinestr,assignstr])
            text += "\n"+Subject.query.filter_by(ID=subject.SubjectID).first().Name
            text += onlinestr
            text += assignstr
            text += "\n================"


    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                   
                    "simpleText": {
                    
                        "text": text
                    
                    }
                   
                }
            ]
        }
    }
    return jsonify(dataSend)



    