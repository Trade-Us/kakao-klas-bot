from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture
from database import db_session

def read_User():
    users = db_session.query(User).order_by(User.ID)
    user_lists=[]
    for user in users:
        user_set=[user.ID, user.Name, user.Password, user.UserKey]
        user_lists.append(user_set)

    return user_lists

 