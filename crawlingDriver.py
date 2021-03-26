from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time, threading
from datetime import datetime


class MyThreadDriver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        options = webdriver.ChromeOptions()
#         options.add_argument("headless")
        #options.add_argument("disable-gpu")
        #options.add_argument("disable-infobars")
#         options.add_argument("no-sandbox")
#         options.add_argument("disable-dev-shm-usage")
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
        
    def printLog(self, string):
        print(threading.currentThread().getName() + string)
#         pass
    def run(self):
        try:
            self.__driver.get(self.base_url)
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
        WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.ID, "loginId")))
        elemId = self.__driver.find_element_by_id("loginId")
        elemId.send_keys(self.id)

        elemPW = self.__driver.find_element_by_id("loginPwd")
        elemPW.send_keys(self.pw)
        elemPW.send_keys(Keys.ENTER)
        self.printLog("로그인 완료...")
#         WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "toplogo")))
        
    def startCrawling(self):
        self.__crawling_data.append(self.crawlingNoticePage())
        self.__crawling_data.append(self.crawlingLecturePage())
        self.printLog("모든 페이지(강의, 공지사항) 크롤링 완료")
        
    ##### Menu Button 접근 및 카테고리 페이지 이동 함수 #####
    def _click_menu_btn(self):
        self.__driver.find_element_by_css_selector('div.toplogo > button').click()
    
    def _access_to_certain_page(self, col, category, row):
        self.__driver\
        .find_element_by_css_selector\
        (f'#navbarHeader > div > div > div:nth-child({col}) > ul > li:nth-child({category}) > ul > li:nth-child({row}) > a').click()
        WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.NAME, "selectSubj")))
    
    ##### Crawling Notice Functions #####
    def getDataNotices(self):
        result = []
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        notices = soup.select("#appModule > table > tbody > tr")
        for notice in notices:
            notice_info = []
            titles = notice.select("td")
            for title in titles:
                notice_info.append(title.text)
            result.append(notice_info)
        return result
    
    def accessNoticePage(self):
        try:
            WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "lft")))
            # 마땅히 할 수 있는 Wqit Tag가 보이지 않는다.
            return self.getDataNotices()
        except Exception as inst:
            print(inst)
            print("공지사항이 없습니다.")
        
    def crawlingNoticePage(self):
        self._click_menu_btn()
        self._access_to_certain_page(2, 1, 2)
        
        notices = []
        
        sub_seq = 1
        while True:
            try:
#                 WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.NAME, "selectSubj")))
                self.__driver.\
                find_element_by_css_selector(f'#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option:nth-child({sub_seq})').click()
            except:
                print("###### NoMoreSubject ######")
                break
            finally:
                notice = self.accessNoticePage()
                if notice is not None:
                    notices = notices + notice
                sub_seq += 1
                
            
        return notices
    
    ##### Crawling Online Lectures Functions #####
    def getDataOnlineLectures(self):
        result = []
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        lectures = soup.select("#appModule > div:nth-child(2) > div.mt-4.mb-4 > div.tablelistbox > table > tbody > tr")[1:]

        for lecture in lectures:
            lecture_info = []
            lists = lecture.select("td")
            for _list in lists:
                lecture_info.append(_list.text.strip())
            result.append(lecture_info)
        return result
 
    def accessLecturePage(self):
        try:
            WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "btn2")))
            return self.getDataOnlineLectures()
        except Exception as inst:
            print(inst)
            print("등록된 강의가 없습니다.")
            
    def crawlingLecturePage(self):
        self._click_menu_btn()
        self._access_to_certain_page(2, 1, 1)
        lectures = []

        sub_seq = 1
        while True:
            try:
                # 와우.. implicitly를 사용하는게 정신건강에 좋을 것 같다.
#                 WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.NAME, "selectSubj")))
                self.__driver.\
                find_element_by_css_selector(f'#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option:nth-child({sub_seq})').click()
                sub_seq += 1
            except:
                print("###### NoMoreSubject ######")
                break
            finally:
                lecture = self.accessLecturePage()
                if lecture is not None:
                    lectures = lectures + lecture

        return lectures       
   
    ##### Crawling Assignments Functions #####
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
            
        return datas
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
        
   
    ##### Crawling Lecture Papers Functions #####    
    def goToAttachmentPage(self):
        #WebDriverWait(self.__driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectlist")))
        url = self.getCssSelector(2, 4)
        self.__driver.find_element_by_css_selector(url).click()
        self.printLog("강의자료 페이지 접근완료")
        time.sleep(1)
        self.goToPrevUrl()
        #time.sleep(1)
    
    
    def goToPrevUrl(self):
        self.__driver.execute_script("window.history.go(-1)")
        
    
    
   
    
    def quitDriver(self):
        self.__driver.quit()
    
    def closeDriver(self):
        print(threading.currentThread().getName() + " 종료")
        self.__driver.close()

        
from read_db import read_User
from database import db_session 
from crawl_models import IDWithSubject, User, Subject, Assignment, Notice, OnlineLecture

def add_Notice(lists):
    for data in lists:
        title=data[1]
        writer=data[3]
        date=datetime.strptime(data[4], '%Y-%m-%d')
        contents=""
        serialNum=data[0]
        subjectID=""
        notice = db_session.query(Notice).filter_by(Title=title, SerialNum=serialNum).first()
        if not notice:
            notice=Notice(title, writer, date, contents, serialNum, subjectID)
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
        myThreadDriver.setCrawlingInfo(data[0], data[2])
        myThreadDriver.start()
        thread_list.append(myThreadDriver)
    
    for t in thread_list:
        notices = t.join()
#         printDatas(notices)
        add_Notice(notices[0])
        
    
    # 앞으로 해야 할 일
    ## 1. 한 아이디 당 모든 과목 크롤링
    ## 2. 멀티 쓰레드 는 위와 같이 하자
    ## 3. Notice 예외 처리! primary key 가 같으면 예외 ㄲ
    ## 4. id, pw 본 db에서 받아오는 함수 추가(다혜)
    ## 5. 받아온 정보를 통해 크롤링 ㄲ


        
if __name__ == "__main__":
    main()
        