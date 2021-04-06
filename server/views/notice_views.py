from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice
from database import db_session
from sqlalchemy import and_, or_

bp = Blueprint('notice', __name__, url_prefix='/notice')


@bp.route('/')
def notice_home():
    return 'Hello'

@bp.route('/recentn', methods=['POST'])
def notice_list():
    content = request.get_json()
    # print(content)
    content = content['action']
    content = content['params']
    name = content['name']
    N = content['num_notice']
    # User 정보 얻어오기
    user_list = User.query.filter_by(Name="모상일").all()
    print(user_list)
    print("##############")
    user_id = user_list[0].ID  

    # User의 Subject 얻어오기
    subject_list = IDWithSubject.query.filter_by(UserID=user_id).all()

    # 사용자가 듣는 과목들만 가져오기 
    ## BackRef 를 고려해보자
    notice_list = Notice.query.filter(or_(
        Notice.SubjectID == f"{subject_list[i].SubjectID}"
        for i in range(len(subject_list))
        )
    ).order_by(Notice.Date.desc())[:N]

    notice_name = []
    # 해당 공지사항의 제목과 과목명을 가져와 notice_name에 이어 붙이기
    for notice in notice_list:
        print(f"######## Notice: {notice}")
        # Notice의 과목명 가져오기  
        subject_name = Subject.query.filter_by(ID=notice.SubjectID).first().Name
        
        notice_name.append([subject_name,notice.Title])
            
    dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : notice[0],
                                    "description" : notice[1]
                                } for notice in notice_name
                            ]
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)

@bp.route('/keyword', methods=['POST'])
def notice_keyword():
    content = request.get_json()
    print(content)
    content = content['action']
    content = content['params']
    keyword = content['키워드']
    name = content['이름']
    
    user_list = User.query.filter_by(Name=name)
    for user in user_list:
        user_id = user.ID    
    subject_list = IDWithSubject.query.filter_by(UserID=user_id)
    notice_name= ""
    for subject in subject_list:
        print(subject)
        notice_list = Notice.query.filter_by(SubjectID=subject.SubjectID)
        for notice in notice_list:
            print(notice)
            print(subject.SubjectID+" : "+notice.Title)    
            if keyword in notice.Title:
                subject_info_list = Subject.query.filter_by(ID=subject.SubjectID)
                for subject_info in subject_info_list:
                    subject_name = subject_info.Name
                notice_name += subject_name + " : "+notice.Title + "\n"
            
        

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