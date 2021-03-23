from database import init_db 
from database import db_session 
from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture

def add_IDWithSubject(crawling):
    data=IDWithSubject(crawling[0], crawling[1])
    db_session.add(data)
    db_session.commit()
def delete_IDWithSubject(userID, subjectID):


def add_User(name, password):
    data=User(name, password)
    db_session.add(data)
    db_session.commit()
def delete_User(name, password):

def add_Subject(name, professor,schedule):
    data=Subject(name, professor,schedule)
    db_session.add(data)
    db_session.commit()
def delete_Subject(name, professor,schedule):

def add_Assignment(title, startDate, endDate, submit, subjectID):
    data=Assignment(title, startDate, endDate, submit, subjectID)
    db_session.add(data)
    db_session.commit()
def delete_Assignment(title, startDate, endDate, submit, subjectID):

def add_Notice(title, writer,date, contents, serialNum, subjectID):
    data=Notice(title, writer,date, contents, serialNum, subjectID)
    db_session.add(data)
    db_session.commit()
def delete_Notice(title, writer,date, contents, serialNum, subjectID):

def add_OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID):
    data=OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID)
    db_session.add(data)
    db_session.commit()
def delete_OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID):

def main():
    add_IDWithSubject("2018203039", "sdh9606")
    add_IDWithSubject("2018203040", "sdh960")

    db_session.close()
    

    #인자로 학번
    #set을 확인해서
    #1. User 테이블에서 학번이랑 pw가져와서 로그인 하기
    #2. 크롤링해서 과목가져와
    #3. 기존에 있는 과목이면 그냥 set에만 저장
    #4. 기존에 없는 과목이면 subject 등록후 set에 저장
    #5. 기능함수

    
if __name__ == "__main__":
    main()

