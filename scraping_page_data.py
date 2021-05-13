from bs4 import BeautifulSoup

## 함수를 따로 두는 이유.. 
## 클래스의 상속으로 중복 코드를 없애기 위함, 그럼 클래스로 작성해야 하는 거 아닌가?
## 파이썬에서는 이런식으로도 가능하기 때문에 ㅗ갠찮
##### Crawling Notice Functions #####
import time
from category_enum import *
def crawling_notice(driver, sub_id, notice):
    notices = driver.find_elements_by_css_selector("#appModule > table > tbody > tr")
    if notices[0].text == "글이 없습니다.":
        print("글이 없음 ")
        return
        # continue
    for i in range(len(notices)):
        info = []
        # title, date, writer, serialNum
        sub_infos = driver.find_elements_by_css_selector(f"#appModule > table > tbody > tr:nth-child({(i+1)}) > td")
        
        for sub_info in sub_infos:
            if sub_info.text:
                info.append(sub_info.text)
            else :
                info.append('-1')

        contents_link = sub_infos[1]
        #contents
        contents_link.click()
        time.sleep(0.5)
        soup = BeautifulSoup( driver.page_source, 'html.parser')
        contents = soup.select_one('div.board_viewDetail > div').get_text()
        info.append(contents)
        info.append(sub_id)
        notice.append(info)
        driver.find_element_by_css_selector("button.btn2").click()
        time.sleep(0.5)
        
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
    [crawling_notice, (2, 1, 2), NOTICE],
    [crawling_online_lecture, (2, 1, 1), ONLINE_LECTURE],
    [crawling_assignments, (2, 1, 6), ASSIGNMENT]
]