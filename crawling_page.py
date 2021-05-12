import time
import threading


#### Crawling Type Function ####
def new_user_crawling_page(subjects, final_result, CrawlingFunction, sub_id, driver):
    # source 에서 공지사항, 등에 두가지가 없나 확인한다
    # 두가지가 있을 경우! 반복문을 통해 전부 크롤링 해온다. 이때는, driver도 같이 넘겨야 함..
    for i, subject in enumerate(subjects):
        sub_id = subject.text.split()[1]
        subject.click()
        time.sleep(0.5)
        
        # 있는지 확인!!!
        # if class paging typeA in source
        
        if i != 0:
            # 없음
            source = driver.page_source 
            final_result = crawling_page_thread(final_result, CrawlingFunction, source, sub_id)
        else:
            pages = []
            pages = driver.find_elements_by_css_selector("ul.paging > li")
            # 있음
            pages = pages[1:-1]
            for page in pages:
                page.click()
                time.sleep(0.5)
                source = driver.page_source 
                final_result = crawling_page_thread(final_result, CrawlingFunction, source, sub_id)
    return final_result

def cur_user_crawling_page(subjects, final_result, CrawlingFunction, sub_id, driver):
    for i, subject in enumerate(subjects):
        sub_id = subject.text.split()[1]
        subject.click()
        time.sleep(0.5)
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