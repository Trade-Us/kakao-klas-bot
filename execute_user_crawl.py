from readDB import read_User, read_NewUser
from updateDB import *

from crawlingDriver import MyThreadDriver
from crawling_page import cur_user_crawling_page, new_user_crawling_page

from crypto_function import SymmetricKeyAgent
import time, threading
def printDatas(datas):
    for category in datas:
        print("######## Category #########")
        for data in category:
            print(data)

def execute_crawl(infoList):
    thread_list = []

    for data in infoList:
        keyAgent = SymmetricKeyAgent()
        myThreadDriver = MyThreadDriver(data[0], keyAgent.decrypt(data[2]), cur_user_crawling_page)
        myThreadDriver.start()
        thread_list.append(myThreadDriver)

    for t in thread_list:
        infos = t.join()
        # printDatas(infos)
        add_Notice(infos[0])
        add_OnlineLecture(t.id, infos[1])
        add_Assignment(t.id, infos[2])

def cur_user_update():
    print("Current User Updating 실행")
    ####### 1시간 당 주기로 돌린다. #######
    infoList = read_User()
    if infoList:
        execute_crawl(infoList)
    period=3600
    timer = threading.Timer(3600, cur_user_update)
    timer.daemon = True
    timer.start()
            
def new_user_create():
    ##### While 무한 루프 돌린다. #####
    infoList = read_NewUser()
    if infoList:
        execute_crawl(infoList)
        ## NewUser에서 삭제 (해당 리스트에 있는 사람만 삭제 해야 겠다.)
        delete_NewUser(infoList)
        ## User에 추가
        add_User(infoList)

if __name__ == "__main__":
    cur_user_update()
    try:
        period=10
        while True:
            new_user_create()
            time.sleep(period)
    except KeyboardInterrupt:
        print("Keyborad Interrupt")
        exit(-1)

        
