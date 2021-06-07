from server.models import *
from database import db_session

def read_User():
    users = db_session.query(User).all()
    user_lists=[]
    for user in users:
        user_set=[user.ID, user.Name, user.Password, user.UserKey]
        user_lists.append(user_set)
    db_session.close()
    return user_lists

def read_NewUser():
    users = db_session.query(NewUser).all()
    user_lists=[]
    for user in users:
        user_set=[user.ID, user.Name, user.Password, user.UserKey]
        user_lists.append(user_set)
    db_session.close()
    return user_lists