import csv
import re
import time
from pprint import pprint

# from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By

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

driver.quit()