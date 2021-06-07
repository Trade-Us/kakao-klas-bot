import time
import threading

# 과목 코드
from category_enum import *
#### Crawling Type Function ####
def user_crawling_page(subjects_length, final_result, CrawlingFunction, category, sub_id, driver):
    # source 에서 공지사항, 등에 두가지가 없나 확인한다
    # 두가지가 있을 경우! 반복문을 통해 전부 크롤링 해온다. 이때는, driver도 같이 넘겨야 함..
    for i in range(subjects_length):
        subject = driver.find_element_by_css_selector(
                f'#appSelectSubj > div.col-md-7 > div > div.col-9 > select > option:nth-of-type({(i+1)})')
        sub_id = subject.text.split()[1]
        subject.click()
        time.sleep(0.5)
        
        # page가 여러개 인 경우 vs 단일 페이지 경우
        if category == NOTICE:
            final_result = crawling_page_thread(final_result, CrawlingFunction, driver, sub_id)
        else:
            # 없음
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
