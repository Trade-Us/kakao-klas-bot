from flask import Blueprint, request, jsonify
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
#from server import db
#from server.models import Notice

bp = Blueprint('notice', __name__, url_prefix='/notice')


@bp.route('/')
def notice_home():
    return 'Hello'

@bp.route('/list')
def notice_list():
    return 'Hello'

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