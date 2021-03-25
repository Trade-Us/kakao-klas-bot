from database import init_db 
from database import db_session 
from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture
from updateDB import add_Assignment, add_IDWithSubject, add_Notice, add_OnlineLecture, add_Subject, add_User


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

