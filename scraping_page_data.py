from bs4 import BeautifulSoup

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