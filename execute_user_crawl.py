from readDB import read_User, read_NewUser
from updateDB import *

from crawlingDriver import MyThreadDriver
from crawling_page import user_crawling_page

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
        myThreadDriver = MyThreadDriver(data[0], keyAgent.decrypt(data[2]), user_crawling_page)
        myThreadDriver.start()
        thread_list.append(myThreadDriver)

    for t in thread_list:
        infos = t.join()
        # printDatas(infos)
        add_Notice(infos[0])
        add_OnlineLecture(t.id, infos[1])
        add_Assignment(t.id, infos[2])
        add_Scores(t.id, infos[3])

def cur_user_update():
    print("Current User Updating 실행")
    ####### 1시간 당 주기로 돌린다. #######
    infoList = read_User()
    if infoList:
        execute_crawl(infoList)
    period=3600
    timer = threading.Timer(period, cur_user_update)
    timer.daemon = True
    timer.start()
            
def new_user_create():
    print("NEW User Updating 실행")
    ##### While 무한 루프 돌린다. #####
    infoList = read_NewUser()
    if infoList:
        execute_crawl(infoList)
        ## NewUser에서 삭제 (해당 리스트에 있는 사람만 삭제 해야 겠다.)
        delete_NewUser(infoList)
        ## User에 추가
        add_User(infoList)
    period=10
    timer = threading.Timer(period, new_user_create)
    timer.daemon = True
    timer.start()
if __name__ == "__main__":
    try:
        cur_user_update()
        new_user_create()
    except KeyboardInterrupt:
        print("Keyborad Interrupt")
        exit(-1)
    while(True):
        pass

        
