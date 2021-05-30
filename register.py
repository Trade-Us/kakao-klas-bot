from crawlingDriver import MyThreadDriver
from database import init_db
from database import db_session
from server.models import User, Subject, IDWithSubject, NewUser
import time
from bs4 import BeautifulSoup
from crypto_function import SymmetricKeyAgent


def register_user(parm_id, name, parm_password, kakaoid):
    # 카카오톡 한 개 user 확인
    check_oneId_oneBot = db_session.query(
        User).filter_by(UserKey=kakaoid).first()
    if check_oneId_oneBot:
      # 카카오톡 2개 이상 id를 등록 하려 하는 경우
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "title": "하나의 아이디만 등록 가능합니다.",
                                    "description": "다른 아이디를 등록하기 원하신다면, 등록해지후 로그인을 시도해주세요 :)"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        return -1, dataSend

    # User 중복 확인
    holdon_user = db_session.query(NewUser).filter_by(ID=parm_id).first()
    if holdon_user:
        # 로그인 실패한 경우
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": [
                                    {
                                        "title": "이미 등록된 유저입니다.",
                                        "description": "현재 사용자의 정보를 읽고 있는 중입니다. 잠시만 기다려주세요^^"
                                    }
                                ]
                            }
                        }
                ]
            }
        }
        return -1, dataSend
    user = db_session.query(User).filter_by(ID=parm_id).first()
    if not user:
        # 로그인 시도 (일단 무조건 성공)
        myThreadDriver = MyThreadDriver(parm_id, parm_password, None)
        myThreadDriver.driver.get('https://klas.kw.ac.kr/')
        myThreadDriver.accessToLogin()
        # 성공시 register
        # time.sleep(1)
        subjects = []

        def check_login_valid():
            nonlocal subjects
            soup = BeautifulSoup(
                myThreadDriver.driver.page_source, 'html.parser')
            subjects = soup.select(
                "#appModule > div > div:nth-child(1) > div:nth-child(2) > ul > li")
            print('pass')
        start = time.time()
        while not subjects:
            if time.time() - start >= 1.2:
                # 여기서 1.5는 로그인 되기까지 1.5초 기다리겠다는 의미임. 따라서,
                # 만약에 id,pw 잘 입력했는데 로그인 실패가 뜨면 1.5보다 크게 하고 (2보다 작게)
                # id,pw 잘못 입력한 경우, 응답시간 초과가 되면 1.5보다 작게 (1보다 크게)
                # 임의로 조절을 부탁합니다! (방법이 없음..ㅜㅜ)
                break
            check_login_valid()
        # 실패시 succeed = false
        print(f"#####check spent time : {(time.time()-start)} #####")
        if not subjects:
            # 로그인 실패한 경우
            dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": [
                                    {
                                        "title": "로그인 실패!",
                                        "description": "ID PW 확인해주세요.."
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
            return -1, dataSend
        # 새 유저인 경우, New_User에 등록..
        keyAgent = SymmetricKeyAgent()
        cipher_pw = keyAgent.encrypt(parm_password)
        new_user = NewUser(ID=parm_id, Name="모상일",
                           Password=cipher_pw, UserKey=kakaoid)
        db_session.add(new_user)

        # print(subjects)
        # 해당 학생의 과목 크롤링
        result = []
        for subject in subjects:
            title = subject.select_one("div.left").text
            splited = title.split()
            result.append(splited)

        # 과목 db 등록
        for subject in result:
            sub = db_session.query(Subject).filter_by(ID=subject[1]).first()
            if not sub:
                s = Subject(ID=subject[1], Name=subject[0],
                            Professor=subject[2], Schedule="")
                db_session.add(s)

            id_sub_set = db_session.query(IDWithSubject).filter_by(
                UserID=parm_id, SubjectID=subject[1]).first()
            if not id_sub_set:
                id_set = IDWithSubject(UserID=parm_id, SubjectID=subject[1])
                db_session.add(id_set)
        db_session.commit()
        db_session.close()
        myThreadDriver.closeDriver()

        return 1, result

    else:
        # User가 이미 등록되어 있는 경우
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "title": "이미 등록된 사용자입니다.",
                                    "description": "ㅎㅎ"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        return -1, dataSend

    # 실패시 오류 처리
