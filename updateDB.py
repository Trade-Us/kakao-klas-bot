from database import db_session
from crawl_models import User, Subject, IDWithSubject, Assignment, OnlineLecture, Notice
from datetime import datetime


def add_IDWithSubject(crawling):
    data = IDWithSubject(crawling[0], crawling[1])
    db_session.add(data)
    db_session.commit()


def delete_IDWithSubject(userID, subjectID):
    pass


def add_User(name, password):
    data = User(name, password)
    db_session.add(data)
    db_session.commit()


def delete_User(name, password):
    pass


def add_Subject(name, professor, schedule):
    data = Subject(name, professor, schedule)
    db_session.add(data)
    db_session.commit()


def delete_Subject(name, professor, schedule):
    pass
    # 항목: 'No', '과제제목', '제출기한', '상태', '조회', '공개과제'


def add_Assignment(lists):
    for data in lists:
        title = data[1]
        submit = data[3]
        subjectID = ""
        # split date into startdate and enddate
        date = data[2].split('~')
        startDate = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S')
        endDate = datetime.strptime(date[1], '%Y-%m-%d %H:%M:%S')

        assignment = Assignment(title, startDate, endDate, submit, subjectID)
        db_session.add(assignment)
        db_session.commit()


def delete_Assignment(title, startDate, endDate, submit, subjectID):
    pass
    # 항목: '번호', '제목', '파일', '작성자', '작성일', '조회수'


def add_Notice(lists):
    for data in lists:
        title = data[1]
        writer = data[3]
        date = datetime.strptime(data[4], '%Y-%m-%d')
        contents = ""
        serialNum = data[0]
        subjectID = data[6]
        notice = db_session.query(Notice).filter_by(
            SerialNum=serialNum, SubjectID=subjectID).first()
        if not notice:
            notice = Notice(title, writer, date, contents,
                            serialNum, subjectID)
            db_session.add(notice)
            db_session.commit()


def delete_Notice(title, writer, date, contents, serialNum, subjectID):
    pass
    # 항목: '주차', '회수', '제목', '목차', '학습기간', '[진도율]학습시간', '강의보기'


def add_OnlineLecture(lists):
    for data in lists:
        progress = data[5]
        contents = ""
        week = data[0]
        episode = data[1]
        subjectID = ""
        # split date into startdate and enddate
        date = data[4].split('~')
        startDate = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S')
        endDate = datetime.strptime(date[1], '%Y-%m-%d %H:%M:%S')

        onlineLecture = OnlineLecture(
            startDate, endDate, progress, contents, week, episode, subjectID)
        db_session.add(onlineLecture)
        db_session.commit()


def delete_OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID):
    pass
