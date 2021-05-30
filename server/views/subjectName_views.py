from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture,NewUser
#from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
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
    i=0
    count = 0
    user_list = User.query.filter_by(UserKey=kakaoid)
    

    for user in user_list:
        print(user.ID)
        user_id = user.ID
        count +=1
    if count == 0:
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
        
        return jsonify(dataSend)
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    print(numbers)
    if parm_subjectName in usersubject_list:
        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel":{
                                "type" : "basicCard",
                                "items" : [
                                    {                            
                                        "description": f"[{parm_subjectName}]\n\n공지사항",
                                        "buttons": [
                                        {
                                            "action": "block",
                                            "label": "최근 공지 보기",
                                            "blockId": "60851c36021d627739d9a7ee"
                                        },
                                    {
                                        "action":  "block",
                                        "label": "키워드 검색",
                                        "blockId": "60851c3e51bb5918f5980367"
                                            }
                                        ]
                                    },
                                    {                                                  
                                        "description": f"[{parm_subjectName}]\n\n과제",
                                        "buttons": [
                                        {
                                        "action": "block",
                                        "label": "진행 중인 과제",
                                        "blockId": "609559c1f1fa0324a1b160aa"
                                        },
                                        {
                                        "action":  "block",
                                        "label": "미제출 과제",
                                        "blockId": "609559d0f1a09324e4b3dcfa"
                                        }
                                        ]                           
                                    },
                                    {
                                        "description": f"[{parm_subjectName}]\n\n온라인 강의",
                                        "buttons": [
                                            {
                                            "action": "block",
                                            "label": "진행 중인 강의",
                                            "blockId": "60955e0ea0ddb07dd0ca47c4"
                                            },
                                            {
                                            "action":  "block",
                                            "label": "미시청 강의",
                                            "blockId": "6096bc0d561a027398d8a57b"
                                            }
                                        ]
                                    }
                                ]
                            }                            
                        }
                    ]
                }
            }
        return jsonify(dataSend)
    elif parm_subjectName in [str(num) for num in numbers]:
        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel":{
                                "type" : "basicCard",
                                "items" : [
                                    {                            
                                        "description": f"[{usersubject_list[int(parm_subjectName)-1]}]\n\n공지사항",
                                        "buttons": [
                                        {
                                            "action": "block",
                                            "label": "최근 공지 보기",
                                            "blockId": "60851c36021d627739d9a7ee"
                                        },
                                    {
                                        "action":  "block",
                                        "label": "키워드 검색",
                                        "blockId": "60851c3e51bb5918f5980367"
                                            }
                                        ]
                                    },
                                    {                                                  
                                        "description": f"[{usersubject_list[int(parm_subjectName)-1]}]\n\n과제",
                                        "buttons": [
                                        {
                                        "action": "block",
                                        "label": "진행 중인 과제",
                                        "blockId": "609559c1f1fa0324a1b160aa"
                                        },
                                        {
                                        "action":  "block",
                                        "label": "미제출 과제",
                                        "blockId": "609559d0f1a09324e4b3dcfa"
                                        }
                                        ]                           
                                    },
                                    {
                                        "description": f"[{usersubject_list[int(parm_subjectName)-1]}]\n\n온라인 강의",
                                        "buttons": [
                                            {
                                            "action": "block",
                                            "label": "진행 중인 강의",
                                            "blockId": "60955e0ea0ddb07dd0ca47c4"
                                            },
                                            {
                                            "action":  "block",
                                            "label": "미시청 강의",
                                            "blockId": "6096bc0d561a027398d8a57b"
                                            }
                                        ]
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
            i+=1
            des+=str(i)+". "+sub
            des+="\n\n"

        dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                            
                            "description": f"이 중 하나를 정확하게 입력해주세요.\n\n(과목이름 또는 번호 입력 가능)\n\n{des}",
                            "buttons": [
                                {
                                "action": "block",
                                "label": "다시 입력",
                                "blockId": "6087e7fdc87b900e56c62ba6"
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
    
    #####
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    #####

    if parm_subjectName in usersubject_list:
        subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    elif parm_subjectName in [str(num) for num in numbers]:
        subject_id = Subject.query.filter_by(Name=usersubject_list[int(parm_subjectName)-1]).first().ID
    #subject_list = IDWithSubject.query.filter_by(SubjectID=subject_id).all()
    print("\nlog:",subject_id)
    notice_list = Notice.query.filter(or_(
        Notice.SubjectID == f"{subject_id}"
        
        )
    ).order_by(Notice.Date.desc())
    print(notice_list)
    notice_name = []
    for notice in notice_list:
        subject_name = Subject.query.filter_by(ID=notice.SubjectID).first().Name
        notice_name.append([subject_name,notice.Title,notice.Contents])
    if len(notice_name) == 0:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                        
                            "text": "해당 과목의 공지사항이 존재하지 않습니다.",
                        
                        }
                    }                 

                ]
            }
        }
        return jsonify(dataSend)
    
    dataSend = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel":{
                            "type" : "basicCard",
                            "items" : [
                                {
                                    #"title" : notice[1],
                                    "description": f"{notice[1]}\n\n{notice[2]}"
                                } for notice in notice_name                                      
                            ]
                        }                            
                    }
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
    
    #####
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    #####
    if parm_subjectName in usersubject_list:
        subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    elif parm_subjectName in [str(num) for num in numbers]:
        subject_id = Subject.query.filter_by(Name=usersubject_list[int(parm_subjectName)-1]).first().ID

    notice_list = Notice.query.filter_by(SubjectID=subject_id)
    notice_name = [] 
    
    for notice in notice_list:
        print(notice)
             
        if parm_keyword in notice.Title:
            
            subject_name = Subject.query.filter_by(ID=notice.SubjectID).first().Name
            notice_name.append([subject_name,notice.Title,notice.Contents])
    
    if len(notice_name) == 0:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                        
                            "text": f"'{parm_keyword}'에 대한 검색 결과가 없습니다.",
                        
                        }
                    }                 

                ]
            }
        }
        return jsonify(dataSend)
    dataSend = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel":{
                            "type" : "basicCard",
                            "items" : [
                                {
                                    #"title" : notice[1],
                                    "description": f"{notice[1]}\n\n{notice[2]}"
                                } for notice in notice_name                                      
                            ]
                        }                            
                    }
                ]
            }
    }

    return jsonify(dataSend)


@bp.route('/assignment_inprogress', methods=['POST'])
def subjectName_assignment_inprogress():
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
    
    #####
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    #####
    if parm_subjectName in usersubject_list:
        subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    elif parm_subjectName in [str(num) for num in numbers]:
        subject_id = Subject.query.filter_by(Name=usersubject_list[int(parm_subjectName)-1]).first().ID

    assignment_list = Assignment.query.filter_by(UserID=user_id,SubjectID=subject_id)
    assignment_name = []
    for assignment in assignment_list:
        #print(notice)      
        if assignment.StartDate <= datetime.now() and assignment.EndDate >= datetime.now():
            if assignment.Submit == True:
                state = "제출"
            else:
                state = "미제출"
            assignment_name.append([assignment.Title,assignment.StartDate.strftime("%Y-%m-%d %H:%M:%S"),assignment.EndDate.strftime("%Y-%m-%d %H:%M:%S"),state])
            print(assignment.StartDate,assignment.EndDate,datetime.now())    

    if len(assignment_name) == 0:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                        
                            "text": "진행 중인 과제가 존재하지 않습니다.",
                        
                        }
                    }                 

                ]
            }
        }
        return jsonify(dataSend)
    
    dataSend = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel":{
                            "type" : "basicCard",
                            "items" : [
                                {
                                    
                                    "description": f"{assignment[0]}\n\n제출기한: {assignment[1]} ~ {assignment[2]}\n\n상태: {assignment[3]}"
                                } for assignment in assignment_name                                      
                            ]
                        }                            
                    }
                ]
            }
    }

    return jsonify(dataSend)

@bp.route('/assignment_incomplete', methods=['POST'])
def subjectName_assignment_incomplete():
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
    
    #####
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    #####
    if parm_subjectName in usersubject_list:
        subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    elif parm_subjectName in [str(num) for num in numbers]:
        subject_id = Subject.query.filter_by(Name=usersubject_list[int(parm_subjectName)-1]).first().ID

    assignment_list = Assignment.query.filter_by(UserID=user_id,SubjectID=subject_id)
    assignment_name = []
    for assignment in assignment_list:
        #print(notice)      
        if assignment.StartDate <= datetime.now() and assignment.EndDate >= datetime.now():
            if assignment.Submit == False:
                state = "미제출"
                assignment_name.append([assignment.Title,assignment.StartDate.strftime("%Y-%m-%d %H:%M:%S"),assignment.EndDate.strftime("%Y-%m-%d %H:%M:%S"),state])
                print(assignment.StartDate,assignment.EndDate,datetime.now())    

    if len(assignment_name) == 0:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                        
                            "text": "미제출 과제가 존재하지 않습니다.",
                        
                        }
                    }                 

                ]
            }
        }
        return jsonify(dataSend)
    
    dataSend = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel":{
                            "type" : "basicCard",
                            "items" : [
                                {
                                    
                                    "description": f"{assignment[0]}\n\n제출기한: {assignment[1]} ~ {assignment[2]}\n\n상태: {assignment[3]}"
                                } for assignment in assignment_name                                      
                            ]
                        }                            
                    }
                ]
            }
    }

    return jsonify(dataSend)

@bp.route('/online_inprogress', methods=['POST'])
def subjectName_online_inprogress():
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
    
    #####
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    #####
    if parm_subjectName in usersubject_list:
        subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    elif parm_subjectName in [str(num) for num in numbers]:
        subject_id = Subject.query.filter_by(Name=usersubject_list[int(parm_subjectName)-1]).first().ID

    online_list = OnlineLecture.query.filter_by(UserID=user_id,SubjectID=subject_id)
    online_name = []
    for online in online_list:
        #print(notice)      
        if online.StartDate <= datetime.now() and online.EndDate >= datetime.now():
            online_name.append([online.Title,online.Contents,online.StartDate.strftime("%Y-%m-%d %H:%M:%S"),online.EndDate.strftime("%Y-%m-%d %H:%M:%S"),online.Progress])
            
    if len(online_name) == 0:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                        
                            "text": "진행중인 온라인 강의가 존재하지 않습니다.",
                        
                        }
                    }                 

                ]
            }
        }
        return jsonify(dataSend)
    
    dataSend = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel":{
                            "type" : "basicCard",
                            "items" : [
                                {
                                    
                                    "description": f"제목: {online[0]}\n\n학습목차: {online[1]}\n\n학습기간: {online[2]} ~ {online[3]}\n\n진도율: {online[4]}"
                                } for online in online_name                                      
                            ]
                        }                            
                    }
                ]
            }
    }

    return jsonify(dataSend)

@bp.route('/online_incomplete', methods=['POST'])
def subjectName_online_incomplete():
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
    
    #####
    usersubject_list = []
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    for subject in subject_list:
        usersubject_list.append(Subject.query.filter_by(ID=subject.SubjectID).first().Name)
    numbers = list(range(1,len(usersubject_list)+1))
    #####
    if parm_subjectName in usersubject_list:
        subject_id = Subject.query.filter_by(Name=parm_subjectName).first().ID
    elif parm_subjectName in [str(num) for num in numbers]:
        subject_id = Subject.query.filter_by(Name=usersubject_list[int(parm_subjectName)-1]).first().ID

    online_list = OnlineLecture.query.filter_by(UserID=user_id,SubjectID=subject_id)
    online_name = []
    for online in online_list:
        #print(notice)      
        if online.StartDate <= datetime.now() and online.EndDate >= datetime.now():
            if online.Progress[1:4] !="100":
                online_name.append([online.Title,online.Contents,online.StartDate.strftime("%Y-%m-%d %H:%M:%S"),online.EndDate.strftime("%Y-%m-%d %H:%M:%S"),online.Progress])
            
    if len(online_name) == 0:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                        
                            "text": "모든 강의를 시청하셨습니다.",
                        
                        }
                    }                 

                ]
            }
        }
        return jsonify(dataSend)
    
    dataSend = {
        "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel":{
                            "type" : "basicCard",
                            "items" : [
                                {
                                    
                                    "description": f"제목: {online[0]}\n\n학습목차: {online[1]}\n\n학습기간: {online[2]} ~ {online[3]}\n\n진도율: {online[4]}"
                                } for online in online_name                                      
                            ]
                        }                            
                    }
                ]
            }
    }

    return jsonify(dataSend)

    