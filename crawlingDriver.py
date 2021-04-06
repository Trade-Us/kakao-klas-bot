from abc import ABC, abstractmethod
from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture
from database import db_session
from read_db import read_User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import threading
from datetime import datetime
import concurrent.futures


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
        self.subject_name = ''
        self.base_url = 'https://klas.kw.ac.kr/'
        self.delay = 3
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.__crawling_data = []
        self.crawlingPage = None

    def setCrawlingPage(self, crawlingPage):
        self.crawlingPage = crawlingPage

    def setCrawlingInfo(self, _id, _pw, crawlingPage):
        self.id = _id
        self.pw = _pw
        self.crawlingPage = crawlingPage

    def printLog(self, string):
        print(threading.currentThread().getName() + string)
#         pass

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

    def startCrawling(self):
        self.__crawling_data.append(self.crawlingNoticePage())
        self.__crawling_data.append(self.crawlingLecturePage())
        self.printLog("모든 페이지(강의, 공지사항) 크롤링 완료")

    ##### Menu Button 접근 및 카테고리 페이지 이동 함수 #####
    def _click_menu_btn(self):
        self.driver.find_element_by_css_selector(
            'div.toplogo > button').click()

    def _access_to_certain_page(self, col, category, row):
        self.driver\
            .find_element_by_css_selector(f'#navbarHeader > div > div > div:nth-child({col}) > ul > li:nth-child({category}) > ul > li:nth-child({row}) > a').click()
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.NAME, "selectSubj")))

    def crawlingNoticePage(self):
        self._click_menu_btn()
        self._access_to_certain_page(2, 1, 2)

        notices = []

        sub_id = ''
        subjects = self.driver.find_elements_by_css_selector(
            '#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option')
        for subject in subjects:

            sub_id = subject.text.split()[1]
            subject.click()
            time.sleep(0.5)
            source = self.driver.page_source
            notice = []
            self.crawlingPage(source, sub_id, notice)

            if notice is not None:
                notices = notices + notice
        self.setCrawlingPage(crawling_online_lecture)
        return notices

    def crawlingLecturePage(self):
        self._click_menu_btn()
        self._access_to_certain_page(2, 1, 1)
        lectures = []
        subjects = self.driver.find_elements_by_css_selector(
            '#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option')
        for subject in subjects:

            sub_id = subject.text.split()[1]
            subject.click()
            time.sleep(0.5)
            source = self.driver.page_source

            lecture = []
            self.crawlingPage(source, sub_id, lecture)

            if lecture is not None:
                lectures = lectures + lecture

        return lectures

    ##### Crawling Assignments Functions #####
    def getDataAssignments(self):
        datas = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        assignments = soup.select('div.tablelistbox > table > tbody > tr')
        for assignment in assignments:
            infos = assignment.select('td')
            i = 0
            data = []
            for info in infos:
                if i > 3:
                    break
                elif i == 1 or i == 3:
                    data.append(info.text)
                # print(info.text)
                i += 1
            datas.append(data)

        return datas

    def goToAssignmentPage(self):
        # 과제 제출 페이지까지 가는 경로
        url = self.getCssSelector(2, 2)
        self.driver.find_element_by_css_selector(url).click()

        try:
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-gray")))
            self.getDataAssignments()
        except:
            pass
        finally:
            self.printLog("과제 페이지 완료")
            self.goToPrevUrl()

    ##### Crawling Lecture Papers Functions #####

    def goToAttachmentPage(self):
        #WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
        url = self.getCssSelector(2, 4)
        self.driver.find_element_by_css_selector(url).click()
        self.printLog("강의자료 페이지 접근완료")
        time.sleep(1)
        self.goToPrevUrl()
        # time.sleep(1)

    def goToPrevUrl(self):
        self.driver.execute_script("window.history.go(-1)")

    def quitDriver(self):
        self.driver.quit()

    def closeDriver(self):
        print(threading.currentThread().getName() + " 종료")
        self.driver.close()

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


def add_Notice(lists):
    for data in lists:
        title = data[1]
        writer = data[3]
        date = datetime.strptime(data[4], '%Y-%m-%d')
        contents = ""
        serialNum = data[0]
        subjectID = data[6]
        notice = db_session.query(Notice).filter_by(
            SerialNum=serialNum, SubjectID=subjectID).first()
        if not notice:
            notice = Notice(title, writer, date, contents,
                            serialNum, subjectID)
            db_session.add(notice)
            db_session.commit()


def printDatas(datas):
    for category in datas:
        print("######## Category #########")
        for data in category:
            print(data)


def main():

    infoList = read_User()
    print(infoList)
#     infoList = [['2018203092', '모상일', 'tkddlf^^12' ]]

    thread_list = []

    for data in infoList:
        myThreadDriver = MyThreadDriver()
        myThreadDriver.setCrawlingInfo(data[0], data[2], crawling_notice)
        myThreadDriver.start()
        thread_list.append(myThreadDriver)

    for t in thread_list:
        notices = t.join()
        printDatas(notices)
        add_Notice(notices[0])

    # 앞으로 해야 할 일
    # 1. 한 아이디 당 모든 과목 크롤링
    # 2. 멀티 쓰레드 는 위와 같이 하자
    # 3. Notice 예외 처리! primary key 가 같으면 예외 ㄲ
    # 4. id, pw 본 db에서 받아오는 함수 추가(다혜)
    # 5. 받아온 정보를 통해 크롤링 ㄲ


if __name__ == "__main__":
    main()
