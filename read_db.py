from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models import User, IDWithSubject, Subject, Assignment, Notice, OnlineLecture

engine = create_engine('sqlite:///information.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def read_User():
    users = session.query(User).order_by(User.ID)
    user_lists=[]
    for user in users:
        user_set=[user.ID, user.Name, user.Password]
        user_lists.append(user_set)

    return user_lists

 