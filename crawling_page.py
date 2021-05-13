import time
import threading

# 과목 코드
from category_enum import *
from copy import deepcopy
#### Crawling Type Function ####
def new_user_crawling_page(subjects_length, final_result, CrawlingFunction, category, sub_id, driver):
    # source 에서 공지사항, 등에 두가지가 없나 확인한다
    # 두가지가 있을 경우! 반복문을 통해 전부 크롤링 해온다. 이때는, driver도 같이 넘겨야 함..
    for i in range(subjects_length):
        subject = driver.find_element_by_css_selector(
                f'#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option:nth-child({(i+1)})')
        sub_id = subject.text.split()[1]
        subject.click()
        time.sleep(0.5)
        
        # page가 여러개 인 경우 vs 단일 페이지 경우
        if category == NOTICE:
            pages = driver.find_elements_by_css_selector("ul.paging > li")
            # 있음
            pages_length = len(pages)-2
            for i in range(pages_length):
                page = driver.find_element_by_css_selector(f"ul.paging > li:nth-child({(i+2)})")
                page.click()
                time.sleep(0.5)
                # 한번더 들어가는 경우 driver vs source
                if category == NOTICE:
                    final_result = crawling_page_thread(final_result, CrawlingFunction, driver, sub_id)
                else:
                    source = driver.page_source 
                    final_result = crawling_page_thread(final_result, CrawlingFunction, source, sub_id)

        else:
            # 없음
            source = driver.page_source 
            final_result = crawling_page_thread(final_result, CrawlingFunction, source, sub_id)
    return final_result

def cur_user_crawling_page(subjects_length, final_result, CrawlingFunction, category, sub_id, driver):
    for i in range(subjects_length):
        subject = driver.find_element_by_css_selector(
                f'#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option:nth-child({(i+1)})')

        sub_id = subject.text.split()[1]
        subject.click()
        time.sleep(0.5)

        if category == NOTICE:
            # Notice 경우
            final_result = crawling_page_thread(final_result, CrawlingFunction, driver, sub_id)
            
        else:
            source = driver.page_source
            final_result = crawling_page_thread(final_result, CrawlingFunction, source, sub_id)
    return final_result

def crawling_page_thread(final_result, CrawlingFunction, source, sub_id):
    result = []
    thread = threading.Thread(
        target= CrawlingFunction, args=(source, sub_id, result))
    thread.start()
    thread.join()
    if result :
        final_result += result
    return final_result
