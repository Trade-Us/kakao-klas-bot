from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome('chromedriver') # 웹드라이버 파일의 경로
driver.implicitly_wait(time_to_wait=5)
path = "https://www.kw.ac.kr/ko/life/notice.jsp?BoardMode=view&DUID=35118&tpage=1&searchKey=2&searchVal=&srCategoryId="
driver.get(path)

req = driver.page_source
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(req, 'html.parser')

###################################

notices = soup.select('.board-list-box > ul > li > div > a')

### 공지사항 링크 ###
links = []
for notice in notices:
    links.append(notice['href'])

### 공지사항 정보 : 카테고리, 제목, 신규, 첨부파일 ###
strong = ""
title = ""
new = False
attatch = False

for notice in notices:
    # 카테고리
    strong = notice.select_one('strong').text if notice.select_one('strong') is not None else ''
    # 제목
    title = notice.text.replace('\n', '').replace('\t', '').strip().split('  ')[0].replace(strong, '')
    # 신규 여부
    new = True if notice.select_one('span.ico-new') is not None else False
    # 첨부파일 여부
    attatch = True if notice.select_one('span.ico-file') is not None else False

    print("strong: ", strong)
    print("title: ", title)
    print("New : ", new)
    print("Attatch : ", attatch)

###################################

# driver.save_screenshot('screenshot.jpg')
driver.quit() # 끝나면 닫아주기

