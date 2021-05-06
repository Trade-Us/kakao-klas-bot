from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture
from database import db_session
from read_db import read_User
from updateDB import *

from crawlingDriver import MyThreadDriver
from crawling_page import cur_user_crawling_page

def printDatas(datas):
    for category in datas:
        print("######## Category #########")
        for data in category:
            print(data)

def main():

    ####### 1시간 당 주기로 돌린다. #######

    infoList = read_User()
    # print(infoList)
    # infoList = [['2018203092', '모상일', 'tkddlf^^12' ]]

    thread_list = []

    for data in infoList:
        myThreadDriver = MyThreadDriver(data[0], data[2], cur_user_crawling_page)
        #myThreadDriver.set_crawling_info(data[0], data[2])
        myThreadDriver.start()
        thread_list.append(myThreadDriver)

    for t in thread_list:
        infos = t.join()
        while True:
            if not t.is_alive():
                # printDatas(infos)
                add_Notice(infos[0])
                add_OnlineLecture(t.id, infos[1])
                add_Assignment(t.id, infos[2])
                break


if __name__ == "__main__":
    main()
