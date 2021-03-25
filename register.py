from threadclass import MyThreadDriver
from database import init_db 
from database import db_session 
from crawl_models import User, Subject, IDWithSubject

def register(id,name,pw):
    user = db_session.query(User).filter_by(ID=id).first()
    if not user:
        u = User(id,name,pw)
        db_session.add(u)
        
    myThreadDriver = MyThreadDriver()
    myThreadDriver.setCrawlingInfo(id,pw,'운영체제')
    subjects = myThreadDriver.get_user_subject()
    for subject in subjects:
        sub = db_session.query(Subject).filter_by(ID=subject[1]).first()
        if not sub:
            s = Subject(subject[1],subject[0],subject[2],"")
            db_session.add(s)
                        
        id_sub_set = db_session.query(IDWithSubject).filter_by(UserID=id,SubjectID=subject[1]).first()
        if not id_sub_set:
            id_set = IDWithSubject(id,subject[1])
            db_session.add(id_set)
    db_session.commit()
    db_session.close()
register("2018203039","심다혜","sdh9606^^")
register("2018203092", "모상일", "tkddlf^^12")
register("2018203054","김범석","k95198245!")
register("2018203067", "이원빈", "wbkaist22!")