from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import threading

from scraping_page_data import crawling_functions
# 테스트 단계에서는, 아이디 등록후, 최근 10개에 대한 정보로 진행하도록 하자
## 일단 여기에 register함수도 포함해서 작성해 놓는다.
## 테스트 내용을 넘기고, New User에 대한 크롤링을 구현한다.

class MyThreadDriver(threading.Thread):
    def __init__(self, _id, _pw, crawling_page_function):
        threading.Thread.__init__(self)
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # options.add_argument("disable-gpu")
        # options.add_argument("disable-infobars")
        options.add_argument("no-sandbox")
        options.add_argument("disable-dev-shm-usage")
        # options.add_argument("enable-experimental-web-platform-features")
        #options.add_argument("default-background-color FFFFFF00")
        self.id = _id
        self.pw = _pw
        self.base_url = 'https://klas.kw.ac.kr/'
        self.delay = 3
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.__crawling_data = []
        self.CrawlingPageFunction = crawling_page_function

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
            # 여기를 수정, new, cur 함수로!
            # 실행 파일에서 해야 하니 삭제
            # self.set_crawling_page_function(function[0])

            self._click_menu_btn()
            self._access_to_certain_page(function[1])

            final_result = []

            sub_id = ''
            subjects = self.driver.find_elements_by_css_selector(
                '#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option')

            # 여기를 dynamic (new, cur)
            final_result = self.CrawlingPageFunction(subjects, final_result, function[0], sub_id, self.driver)
            
            self.__crawling_data.append(final_result)

    # Sub Function
    def goToPrevUrl(self):
        self.driver.execute_script("window.history.go(-1)")

    def quitDriver(self):
        self.driver.quit()

    def closeDriver(self):
        print(threading.currentThread().getName() + " 종료")
        self.driver.close()

