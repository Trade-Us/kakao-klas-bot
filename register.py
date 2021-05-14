from crawlingDriver import MyThreadDriver
from database import init_db 
from database import db_session 
from server.models import User, Subject, IDWithSubject, NewUser
import time
from bs4 import BeautifulSoup
from crypto_function import SymmetricKeyAgent

def register_user(parm_id,name,parm_password, kakaoid):

    # User 중복 확인
    user = db_session.query(User).filter_by(ID=parm_id).first()
    if not user:
        keyAgent = SymmetricKeyAgent()
        cipher_pw = keyAgent.encrypt(parm_password)
        user = User(ID=parm_id,Name="모상일",Password=cipher_pw, UserKey=kakaoid)
        new_user = NewUser(ID=parm_id, Name="모상일", Password=cipher_pw)
        db_session.add(user)
        db_session.add(new_user)

    else:
        # User가 이미 등록되어 있는 경우
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : "이미 등록된 사용자입니다.",
                                    "description" : "ㅎㅎ"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        return -1, dataSend
    # check_oneId_oneBot = db_session.query(User).filter_by(UserKey=kakaoid).first()
    # if check_oneId_oneBot:
    #   #카카오톡 2개 이상 id를 등록 하려 하는 경우
    #     dataSend = {
    #         "version": "2.0",
    #         "template": {
    #             "outputs": [
    #                 {
    #                     "carousel": {
    #                         "type" : "basicCard",
    #                         "items": [
    #                             {
    #                                 "title" : "봇에서는 하나의 아이디만 등록 가능합니다.",
    #                                 "description" : "ㅎㅎ"
    #                             }
    #                         ]
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    #     return -1, dataSend
    # 로그인 시도 (일단 무조건 성공)
    myThreadDriver = MyThreadDriver(parm_id, parm_password, None)
    myThreadDriver.driver.get('https://klas.kw.ac.kr/')
    myThreadDriver.accessToLogin()
    # 성공시 register
    time.sleep(2)
    soup = BeautifulSoup(myThreadDriver.driver.page_source, 'html.parser')
    subjects = soup.select("#appModule > div > div:nth-child(1) > div:nth-child(2) > ul > li")
    # 실패시 succeed = false
    if not subjects:
        # 로그인 실패한 경우
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : "로그인 실패!",
                                    "description" : "ID PW 확인해주세요.."
                                }
                            ]
                        }
                    }
                ]
            }
        }
        return -1, dataSend
    
    # print(subjects)
    result = []
    for subject in subjects:
        title = subject.select_one("div.left").text
        splited = title.split()
        result.append(splited)

    for subject in result:
        sub = db_session.query(Subject).filter_by(ID=subject[1]).first()
        if not sub:
            s = Subject(ID=subject[1],Name=subject[0],Professor=subject[2],Schedule="")
            db_session.add(s)
                        
        id_sub_set = db_session.query(IDWithSubject).filter_by(UserID=parm_id,SubjectID=subject[1]).first()
        if not id_sub_set:
            id_set = IDWithSubject(UserID=parm_id,SubjectID=subject[1])
            db_session.add(id_set)
    db_session.commit()
    db_session.close()
    myThreadDriver.closeDriver()

    return 1, result
    # 실패시 오류 처리
# _, v = register_user("2018203092", "df", "tkddlf^^12", "sdf")
# print(v)