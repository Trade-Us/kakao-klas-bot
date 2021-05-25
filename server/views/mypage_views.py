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
    kakaoid = content['userRequest']['user']['id']
    user = User.query.filter_by(UserKey=kakaoid).first()
    if not user:
        return -1
    user_id = user.ID

    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    mypage_list = []
    for subject in subject_list:
        temp_assign_list = []
        temp_online_list = []
        assignment_list = Assignment.query.filtr_by(UserID=user_id,SubjectID=subject.ID)
        for assignment in assignment_list:      
            if assignment.StartDate <= datetime.now() and assignment.EndDate >= datetime.now():
                if assignment.Submit == True:
                    state = "제출"
                else:
                    state = "미제출"
                temp_assign_list.append(assignment.Title)
                temp_assign_list.append(state)
                #print(assignment.StartDate,assignment.EndDate,datetime.now())
        online_list = OnlineLecture.query.filter_by(UserID=user_id)
        for online in online_list:
            if online.StartDate <= datetime.now() and online.EndDate >= datetime.now():
                temp_online_list.append(online.Title)
                temp_online_list.append(online.Progress)
        if len(temp_assign_list) > 0 or len(temp_online_list) >0:
            mypage_list.append([subject.Name,temp_online_list,temp_assign_list])
        


    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type" : "basicCard",
                        "items": [
                            {
                                
                                "description" : f"{mypage[0]}\n\n강의\n\n{""for onlineL in mypage[1]}"
                            } for mypage in mypage_list
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)



    