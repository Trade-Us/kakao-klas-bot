# from cryptography.fernet import Fernet

# def write_key():
#     """
#     Generates a key and save it into a file
#     """
#     key = Fernet.generate_key()
#     with open("./keystore/key.key", "wb") as key_file:
#         key_file.write(key)

# write_key()
from category_enum import *
page_info = ["crawling_assignments", (1, 2, 2), SCORE_CHECK]

from crawlingDriver import MyThreadDriver
from bs4 import BeautifulSoup

myThreadDriver = MyThreadDriver("2018203092", "tkddlf^^12", None)
myThreadDriver.driver.get('https://klas.kw.ac.kr/')
login_check = myThreadDriver.accessToLogin()
myThreadDriver._click_menu_btn()
myThreadDriver._access_to_certain_page(page_info[1], page_info[2])

page = myThreadDriver.driver.page_source
soup = BeautifulSoup(page, "html.parser")

datas = soup.select("#hakbu > table.AType")[0]
infos = datas.select("tbody > tr")
all_result = []
for data in infos:
    result = data.text.split(' ')
    one_result = []
    for i in range(1, len(result), 2):
        one_result.append(result[i])
        # print(result[i])
    all_result.append(one_result)
from updateDB import *
add_Scores("2018203092", all_result)


# print(datas[0])
myThreadDriver.quitDriver()