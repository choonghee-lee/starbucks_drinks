import csv
import re
import time
from pprint import pprint

from selenium import webdriver

TARGET_URL_LIST   = "https://www.starbucks.co.kr/menu/drink_list.do"
TARGET_URL_DETAIL = "https://www.starbucks.co.kr/menu/drink_view.do?product_cd="

BS_PARSER = "html.parser"

IMPLICIT_WAIT = 5

# 스타벅스 음료 리스트 페이지 접속
driver = webdriver.Chrome()
driver.get(TARGET_URL_LIST)
driver.implicitly_wait(IMPLICIT_WAIT)

# 음료 제품 번호 가져오기
go_drink_views = driver.find_elements_by_class_name('goDrinkView')
product_numbers = [a.get_attribute('prod') for a in go_drink_views]

for product_number in product_numbers:
    driver.get(TARGET_URL_DETAIL + product_number)

    # 한글 이름, 영어 이름
    name_kr, name_en = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/h4').text.split('\n')
    
    # TODO: description1 == description2
    description1_text = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/p').text.split('\n')
    description2_text = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]').text.split('\n')
    description1      = ' '.join(description1_text)
    description2      = ' '.join(description2_text)

    # 사이즈 정보
    size_text = driver.find_element_by_xpath('//*[@id="product_info01"]').text
    size = re.sub('[^\w]|ml|fl|oz', ' ', size_text).split()
    # pprint(size) # TODO: 현재는 리스트!
    


driver.quit()