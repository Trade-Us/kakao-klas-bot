from database import db_session
from crawl_models import *
from datetime import datetime


def add_IDWithSubject(crawling):
    data = IDWithSubject(crawling[0], crawling[1])
    db_session.add(data)
    db_session.commit()


def delete_IDWithSubject(userID, subjectID):
    pass


def add_User(ID):
    data = User(name, password)
    db_session.add(data)
    db_session.commit()


def delete_User(ID):
    pass

def add_NewUser(ID):
    data = User(name, password)
    db_session.add(data)
    db_session.commit()


def delete_NewUser(ID):
    if ID == "all":
        db_session.query(NewUser).delete()
        db_session.commit()
    else:
        pass

def add_Subject(name, professor, schedule):
    data = Subject(name, professor, schedule)
    db_session.add(data)
    db_session.commit()


def delete_Subject(name, professor, schedule):
    pass
    # 항목: 'No', '과제제목', '제출기한', '상태', '조회', '공개과제'


def add_Assignment(userID, lists):
    for data in lists:
        title = data[1]
        submit = True if data[3] == '제출' else False
        subjectID = data[6]
        # split date into startdate and enddate
        date = data[2].split('~')
        startDate = datetime.strptime(date[0].strip(), '%Y-%m-%d %H:%M:%S')
        endDate = datetime.strptime(date[1].strip(), '%Y-%m-%d %H:%M:%S')

        assignment = db_session.query(Assignment).filter_by(UserID=userID, Title=title, SubjectID=subjectID).first()
        if not assignment:
            assignment = Assignment(userID, title, startDate, endDate, submit, subjectID)
            db_session.add(assignment)
            db_session.commit()


def delete_Assignment(title, startDate, endDate, submit, subjectID):
    pass
    # 항목: '번호', '제목', '파일', '작성자', '작성일', '조회수'


def add_Notice(lists):
    for data in lists:
        title = data[0]
        writer = data[1]
        date = datetime.strptime(data[2], '%Y-%m-%d %H:%M')
        contents = data[3]
        subjectID = data[4]
        notice = db_session.query(Notice).filter_by(
            Title=title, SubjectID=subjectID).first()
        if not notice:
            notice = Notice(title, writer, date, contents, subjectID)
            db_session.add(notice)
            db_session.commit()


def delete_Notice(title, writer, date, contents, serialNum, subjectID):
    pass
    # 항목: '주차', '회수', '제목', '목차', '학습기간', '[진도율]학습시간', '강의보기'


def add_OnlineLecture(userID, lists):
    for data in lists:
        progress = data[5]
        title = data[2]
        contents = data[3]
        week = data[0]
        episode = data[1]
        subjectID = data[7]
        # split date into startdate and enddate
        date = data[4].split('~')
        startDate = datetime.strptime(date[0].strip(), '%Y-%m-%d %H:%M')
        endDate = datetime.strptime(date[1].strip(), '%Y-%m-%d %H:%M')

        onlineLecture = db_session.query(OnlineLecture).filter_by(UserID=userID, Week=week, Episode=episode, SubjectID=subjectID).first()
        if not onlineLecture:
            onlineLecture = OnlineLecture(userID,title, startDate, endDate, progress, contents, week, episode, subjectID)
            db_session.add(onlineLecture)
            db_session.commit()


def delete_OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID):
    pass
