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

def add_Notice(data):
    title=data[1]
    writer=data[3]
    date=data[4]
    contents=""
    serialNum=data[0]
    subjectID=""

    notice=Notice(title, writer,date, contents, serialNum, subjectID)
    db_session.add(notice)
    db_session.commit()

def delete_Notice(title, writer,date, contents, serialNum, subjectID):

def add_OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID):
    data=OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID)
    db_session.add(data)
    db_session.commit()
def delete_OnlineLecture(startDate, endDate, progress, contents, week, episode, subjectID):
