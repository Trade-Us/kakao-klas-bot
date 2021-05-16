from bs4 import BeautifulSoup

## 함수를 따로 두는 이유.. 
## 클래스의 상속으로 중복 코드를 없애기 위함, 그럼 클래스로 작성해야 하는 거 아닌가?
## 파이썬에서는 이런식으로도 가능하기 때문에 ㅗ갠찮
##### Crawling Notice Functions #####
import time
from category_enum import *

def crawl_detail_notice(source, info):
    soup = BeautifulSoup(source, 'html.parser')
    # 데이터 먼저 크롤링 
    title = soup.select_one("div.board_view_header > h2").text
    sub = soup.select_one("div.board_view_header > div").get_text()\
    .replace("작성자 : ", '').replace("등록일 :", '').replace("조회수 :", '').split()
    writer = sub[0]
    date = f"{sub[1]} {sub[2]}"
    contents = soup.select_one('div.board_viewDetail > div').get_text()
    for entity in [title, writer, date, contents]:
        info.append(entity)
    # 이전 글 존재 여부 체크
    prev_notice = soup.select_one("#appModule > div.next_prev_box > dl:nth-child(1) > dd")
    print(prev_notice.text)
    return True if prev_notice.text.strip() == "이전글이 없습니다." else False 

def crawling_notice(driver, sub_id, notice):
    notices = driver.find_elements_by_css_selector("#appModule > table > tbody > tr")
    if notices[0].text == "글이 없습니다.":
        # print("글이 없음 ")
        return
        # continue
    start_crawl_notice = ''
    # 중요 표시 확인 로직
    for i in range(len(notices)):
        star_notice = driver.find_elements_by_css_selector(f"#appModule > table > tbody > tr:nth-child({(i+1)}) > td")
        no_star = star_notice[0].text
        link = star_notice[1]
        if no_star :
            # 중요 표시 아닌 경우, 그만
            start_crawl_notice = link # 중요 표시 그 다음 notice를 저장
            break
        else:
            info = []
            # 중요 표시 인 경우, 들어가서 해당 데이터 담는다.
            link.click()
            time.sleep(0.5)
            crawl_detail_notice(driver.page_source, info)
            info.append(sub_id)
            notice.append(info)
            driver.find_element_by_css_selector("button.btn2").click()
            time.sleep(0.5)
    # 나머지 데이터 크롤링
    # 시작 할 페이지 입장
    start_crawl_notice.click()
    time.sleep(0.5)
    # 반복 ; until 이전 글이 없습니다.
    while True:
        info = []
        # 데이터 크롤링
        prev_page_not_exist = crawl_detail_notice(driver.page_source, info)
        info.append(sub_id)
        notice.append(info)
        if prev_page_not_exist:
            # 이전 페이지 없음  
            break 
        driver.find_element_by_css_selector("#appModule > div.next_prev_box > dl:nth-child(1) > dd").click()
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
    info = []
    for i, data in enumerate(datas):
        titles = data.select('td')
        if i % 2 == 0:
            info.clear()
            for title in titles:
                if title.text == "출제된 레포트가 없습니다.":
                    return
                info.append(title.text)
        else:
            info.append(titles[0].text)
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