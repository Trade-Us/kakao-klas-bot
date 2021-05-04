from abc import ABC, abstractmethod
from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture
from database import db_session

from read_db import read_User
from updateDB import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import threading

# 테스트 단계에서는, 아이디 등록후, 최근 10개에 대한 정보로 진행하도록 하자
## 일단 여기에 register함수도 포함해서 작성해 놓는다.
## 테스트 내용을 넘기고, New User에 대한 크롤링을 구현한다.

class MyThreadDriver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # options.add_argument("disable-gpu")
        # options.add_argument("disable-infobars")
        options.add_argument("no-sandbox")
        options.add_argument("disable-dev-shm-usage")
        # options.add_argument("enable-experimental-web-platform-features")
        #options.add_argument("default-background-color FFFFFF00")
        self.id = ''
        self.pw = ''
        self.base_url = 'https://klas.kw.ac.kr/'
        self.delay = 3
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.__crawling_data = []
        self.CrawlingFunction = None

    def set_crawling_page_function(self, crawling_function):
        self.CrawlingFunction = crawling_function

    def set_crawling_info(self, _id, _pw):
        self.id = _id
        self.pw = _pw

    def printLog(self, string):
        print(threading.currentThread().getName() + string)
#         pass
    ##### Thread 실행 및 대기 함수 #####

    def run(self):
        try:
            self.driver.get(self.base_url)
            self.accessToLogin()
            self.startCrawling()
        except Exception as inst:
            print(inst)
        finally:
            self.closeDriver()

    def join(self):
        threading.Thread.join(self)
        return self.__crawling_data

    def startCrawling(self):
        # self.__crawling_data.append(self.crawling_notice_page())
        # self.__crawling_data.append(self.crawling_online_lecture_page())
        self.crawling_page()
        self.printLog("모든 페이지(강의, 공지사항) 크롤링 완료")

    ##### Klas.kw.ac.kr 접속 및 로그인 #####
    def accessToLogin(self):
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.ID, "loginId")))
        elemId = self.driver.find_element_by_id("loginId")
        elemId.send_keys(self.id)

        elemPW = self.driver.find_element_by_id("loginPwd")
        elemPW.send_keys(self.pw)
        elemPW.send_keys(Keys.ENTER)
        self.printLog("로그인 완료...")
#         WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "toplogo")))

    ##### Menu Button 접근 및 카테고리 페이지 이동 함수 #####
    def _click_menu_btn(self):
        self.driver.find_element_by_css_selector(
            'div.toplogo > button').click()

    def _access_to_certain_page(self, tuple):
        self.driver\
            .find_element_by_css_selector(f'#navbarHeader > div > div > div:nth-child({tuple[0]}) > ul > li:nth-child({tuple[1]}) > ul > li:nth-child({tuple[2]}) > a').click()
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.NAME, "selectSubj")))

    ##### Page 크롤링 기능 함수 #####
    def crawling_page(self):
        for function in crawling_functions:
            self.set_crawling_page_function(function[0])

            self._click_menu_btn()
            self._access_to_certain_page(function[1])

            final_result = []

            sub_id = ''
            subjects = self.driver.find_elements_by_css_selector(
                '#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option')

            for i, subject in enumerate(subjects):

                sub_id = subject.text.split()[1]
                subject.click()
                time.sleep(0.5)
                source = self.driver.page_source
                result = []
                thread = threading.Thread(
                    target=self.CrawlingFunction, args=(source, sub_id, result))
                thread.start()
                while True:
                    if not thread.is_alive():
                        if result is not None:
                            final_result += result
                        break
            # time.sleep(0.5)
            self.__crawling_data.append(final_result)

    # Sub Function
    def goToPrevUrl(self):
        self.driver.execute_script("window.history.go(-1)")

    def quitDriver(self):
        self.driver.quit()

    def closeDriver(self):
        print(threading.currentThread().getName() + " 종료")
        self.driver.close()

## 함수를 따로 두는 이유.. 
## 클래스의 상속으로 중복 코드를 없애기 위함, 그럼 클래스로 작성해야 하는 거 아닌가?
## 파이썬에서는 이런식으로도 가능하기 때문에 ㅗ갠찮
##### Crawling Notice Functions #####

def crawling_notice(page_source, sub_id, notice):

    soup = BeautifulSoup(page_source, 'html.parser')
    datas = soup.select("#appModule > table > tbody > tr")
    for data in datas:
        info = []
        titles = data.select("td")
        for title in titles:
            if title.text == "글이 없습니다.":
                return
            info.append(title.text)
        info.append(sub_id)
        notice.append(info)

##### Crawling Online Lectures Functions #####

def crawling_online_lecture(page_source, sub_id, online_lecture):
    soup = BeautifulSoup(page_source, 'html.parser')
    datas = soup.select(
        "#appModule > div:nth-child(2) > div.mt-4.mb-4 > div.tablelistbox > table > tbody > tr")[1:]

    for data in datas:
        info = []
        titles = data.select("td")
        for title in titles:
            if title.text == "등록된 온라인강의가 없습니다.":
                return
            info.append(title.text.strip())
        info.append(sub_id)
        online_lecture.append(info)
##### Crawling Assignments Functions #####

def crawling_assignments(page_source, sub_id, assignment):

    soup = BeautifulSoup(page_source, 'html.parser')
    datas = soup.select('div.tablelistbox > table > tbody > tr')
    for data in datas:
        info = []
        titles = data.select('td')
        for title in titles:
            if title.text == "출제된 레포트가 없습니다.":
                return
            info.append(title.text)
        if info[0] != "-":
            info.append(sub_id)
            assignment.append(info)
        
##### Crawling Lecture Papers Functions #####

def crawling_attachments(page_source, sub_id, attachment):
    #WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
    url = self.getCssSelector(2, 4)
    self.driver.find_element_by_css_selector(url).click()
    self.printLog("강의자료 페이지 접근완료")
    time.sleep(1)
    self.goToPrevUrl()
    # time.sleep(1)      


crawling_functions = [
    [crawling_notice, (2, 1, 2)],
    [crawling_online_lecture, (2, 1, 1)],
    [crawling_assignments, (2, 1, 6)]
]

### 실행! ###


def printDatas(datas):
    for category in datas:
        print("######## Category #########")
        for data in category:
            print(data)


def main():

    infoList = read_User()
    # print(infoList)
    # infoList = [['2018203092', '모상일', 'tkddlf^^12' ]]

    thread_list = []

    for data in infoList:
        myThreadDriver = MyThreadDriver()
        myThreadDriver.set_crawling_info(data[0], data[2])
        myThreadDriver.start()
        thread_list.append(myThreadDriver)

    for t in thread_list:
        infos = t.join()
        while True:
            if not t.is_alive():
                printDatas(infos)
                add_Notice(infos[0])
                add_OnlineLecture(t.id, infos[1])
                add_Assignment(t.id, infos[2])
                break

    # 앞으로 해야 할 일
    # register 경우, 일단 User의 정보만 (register함수) 통신시의 크롤링했을때, 잘 버티는지 확인하라
    # 왜냐하면, 로그인이 되는지 확인을 해 보아야 하기 때문이다.

    # 만약 잘 된다면 굳
    # 안된다면, 과목 정보 가져오는 것을 제외한다.

    # 해결이 되면, 일단 새로운 User 테이블에서 최근10개(현재 드라이버)만 가져올 수 있도록 한다.

    # 이후, 새로운 User에 대해 모든 정보를 얻어오는 크롤링 드라이버를 구현한다.


if __name__ == "__main__":
    main()
