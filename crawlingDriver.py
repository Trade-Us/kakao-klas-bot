from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time, threading
from datetime import datetime

from database import init_db 
from database import db_session 
from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture

class MyThreadDriver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        #options.add_argument("disable-gpu")
        #options.add_argument("disable-infobars")
        options.add_argument("no-sandbox")
        options.add_argument("disable-dev-shm-usage")
        #options.add_argument("enable-experimental-web-platform-features")
        #options.add_argument("default-background-color FFFFFF00")
        self.id = ''
        self.pw = ''
        self.subject_name = ''
        self.base_url = 'https://klas.kw.ac.kr/'
        self.delay = 3
        self.__driver = webdriver.Chrome(options=options)
        self.__driver.implicitly_wait(10)
        self.__crawling_data = []
    
    def setCrawlingInfo(self, _id, _pw):
        self.id = _id
        self.pw = _pw
#         self.subject_name = _subject_name
        
    def printLog(self, string):
        print(threading.currentThread().getName() + string)
#         pass
    
    def run(self):
        try:
            self.__driver.get(self.base_url)
            self.accessToLogin()
            self.startCrawling()
#             self._getIntoSubject()
            # 온라인 강의 크롤링
#             self.goToAssignmentPage()
            # 과제 크롤링
#             self.__crawling_data.append(self.goToNoticePage())
            # 공지사항 크롤링
#             self.goToAttachmentPage()
            # 첨부자료 크롤링
        except Exception as inst:
            print(inst)
        finally:
            self.closeDriver()
    
    def join(self):
        threading.Thread.join(self)
        return self.__crawling_data
    
    def accessToLogin(self):
        WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.ID, "loginId")))
        #time.sleep(1)
        elemId = self.__driver.find_element_by_id("loginId")
        elemId.send_keys(self.id)

        elemPW = self.__driver.find_element_by_id("loginPwd")
        elemPW.send_keys(self.pw)
        elemPW.send_keys(Keys.ENTER)
        self.printLog("로그인 완료...")
        
    def getIntoSubject(self):
#         WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
#         self.__driver.find_element_by_css_selector(f"ul.subjectlist > li:nth-child({subject_seq}) > div.left").click()
        try:
            WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "btn2")))
            return self.getDataOnlineLectures()
        except Exception as inst:
            print(inst)
            print("등록된 강의가 없습니다.")
            return
    
    def crawlings(self):
        datas = []
        datas.append(self.getIntoSubject())
        datas.append(self.goToNoticePage())
        self.__crawling_data.append(datas)
        self.__driver.get(self.base_url)
#         print(self.__driver.current_url)
        self.printLog("모든 페이지(강의, 공지사항) 크롤링 완료")

    def startCrawling(self):
        sub_seq = 1
        while True:
            try:
                WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
                self.__driver.find_element_by_css_selector(f"ul.subjectlist > li:nth-child({sub_seq}) > div.left").click()
                sub_seq += 1
            except Exception as inst:
                print(inst)
                print("No More Subject")
                break
            self.crawlings()
            # While True 로 바꾸어서, 과목이 나오지 않을 때까지 한다.
            
#     def _getIntoSubject(self):
#         # 해당 과목 페이지로 진입
#         WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
#         self.__driver.find_element_by_css_selector("ul.subjectlist > li > div.left").click()
#         print("Breaking Point 1")
# #         WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.NAME, "selectSubj")))
#         WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "btn2")))
#         print("Breaking Point 2")
#         for i in range(3):
#             try:
#                 option = self.__driver.find_element_by_css_selector("select[name=selectSubj]")
#                 option.click()
#                 option.find_element_by_css_selector("option:nth-child(" + str(i+1) + ")").click()
#                 print("Breaking Point 3")
# #                 WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "btn2")))
#                 self.getDataOnlineLectures()
#                 self.__crawling_data.append(self.goToNoticePage())
#             except Exception as inst:
#                 print(inst)
#                 break
#             finally:
#                 self.printLog("모든 페이지 크롤링 완료")
# #                 self.goToPrevUrl(-2)
# #                 self.__driver.get('https://klas.kw.ac.kr/')
# #                 time.sleep(2)
# #                 print(self.__driver.current_url)
    
    # ---- 과제, 공지사항, 등등 페이지로 넘어갈 때에는 크롤링 하기전에만 Wait을 해주면 괜찮다. -----#
    # -- 뒤로가기 시에는 get 메소드가 아니기 때문에 Explicit Wait 작동 X -- #
    # 과제 경로 -> 2, 2
    def goToAssignmentPage(self):
        ## 과제 제출 페이지까지 가는 경로
        url = self.getCssSelector(2, 2)
        self.__driver.find_element_by_css_selector(url).click()
        
        try:
            WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-gray")))
            self.getDataAssignments()
        except:
            pass
        finally:
            self.printLog("과제 페이지 완료")
            self.goToPrevUrl()
        
    # 공지사항
    def goToNoticePage(self):
        # WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "notice-list")))
        url = ".notice-list > div.bodtitle > a"
        self.__driver.find_element_by_css_selector(url).click()
        
        try:
            # Wait Clause
            WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "lft")))
            # 마땅히 할 수 있는 Wqit Tag가 보이지 않는다.
            return self.getDataNotices()
        except Exception as inst:
            print(inst)
            print("lft tag가 없음")
        finally:
            self.printLog("공지사항 페이지 완료")
            self.goToPrevUrl()
        #time.sleep(1)
        
    def goToAttachmentPage(self):
        #WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
        url = self.getCssSelector(2, 4)
        self.__driver.find_element_by_css_selector(url).click()
        self.printLog("강의자료 페이지 접근완료")
        time.sleep(1)
        self.goToPrevUrl()
        #time.sleep(1)
    
    def getCssSelector(self, div, li):
        return ".subjectpresentbox > div.tablelistbox > div > div:nth-child({}) > ul > li:nth-child({}) > a".format(div, li)
    
    def goToPrevUrl(self):
        self.__driver.execute_script("window.history.go(-1)")
        
    def getDataOnlineLectures(self):
        result = []
        soup = BeautifulSoup(self.__driver.page_source, 'lxml')
        lectures = soup.select("#appModule > div:nth-child(2) > div.mt-4.mb-4 > div.tablelistbox > table > tbody > tr")[1:]

        for lecture in lectures:
            lecture_info = []
            lists = lecture.select("td")
            for _list in lists:
                lecture_info.append(_list.text.strip())
            result.append(lecture_info)
#         print(result)
        return result
    def getDataAssignments(self):
        datas = []
        soup = BeautifulSoup(self.__driver.page_source, 'lxml')
        assignments = soup.select('div.tablelistbox > table > tbody > tr')
        for assignment in assignments:
            infos = assignment.select('td')
            i = 0
            data = []
            for info in infos:
                if i > 3: break
                elif i == 1 or i == 3:
                    data.append(info.text)
                #print(info.text)
                i += 1
            datas.append(data)
        print(datas)
#         return datas
    def getDataNotices(self):
        result = []
        soup = BeautifulSoup(self.__driver.page_source, 'lxml')
        notices = soup.select("#appModule > table > tbody > tr")
        for notice in notices:
            notice_info = []
            titles = notice.select("td")
            for title in titles:
                notice_info.append(title.text)
            result.append(notice_info)
        
#         self.add_Notice(result)
        return result
    
    def quitDriver(self):
        self.__driver.quit()
    
    def closeDriver(self):
        print(threading.currentThread().getName() + " 종료")
        self.__driver.close()

        
from read_db import read_User
def add_Notice(lists):
    for data in lists:
        title=data[1]
        writer=data[3]
        date=datetime.strptime(data[4], '%Y-%m-%d')
        contents=""
        serialNum=data[0]
        subjectID=""

        notice=Notice(title, writer, date, contents, serialNum, subjectID)
        db_session.add(notice)
        db_session.commit()
def printDatas(datas):
    for subject in datas:
        print("######## #########")
        
        for category in subject:
            print(">>")
            if category is None:
                print("없음")
                continue
            for data in category:
                print(data)
def main():
    
#     infoList = read_User()
    infoList = [['2018203092', '모상일', 'tkddlf^^12' ]]

    thread_list = []
    
    for data in infoList:
        myThreadDriver = MyThreadDriver()
        myThreadDriver.setCrawlingInfo(data[0], data[2])
        myThreadDriver.start()
        thread_list.append(myThreadDriver)
    
    for t in thread_list:
        notices = t.join()
        printDatas(notices)
        print("###############")
#         add_Notice(notices[0])
        
    
    # 앞으로 해야 할 일
    ## 1. 한 아이디 당 모든 과목 크롤링
    ## 2. 멀티 쓰레드 는 위와 같이 하자
    ## 3. Notice 예외 처리! primary key 가 같으면 예외 ㄲ
    ## 4. id, pw 본 db에서 받아오는 함수 추가(다혜)
    ## 5. 받아온 정보를 통해 크롤링 ㄲ


        
if __name__ == "__main__":
    main()
        