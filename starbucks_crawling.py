import csv
import re
import time

from selenium import webdriver

TARGET_URL_LIST   = "https://www.starbucks.co.kr/menu/drink_list.do"
TARGET_URL_DETAIL = "https://www.starbucks.co.kr/menu/drink_view.do?product_cd="
BS_PARSER         = "html.parser"
IMPLICIT_WAIT     = 5
TIME_SLEEP        = 1
CSV_FILENAME      = "starbucks_drinks.csv"

# CSV 파일 열기
csv_open   = open(CSV_FILENAME, "w+", encoding="utf-8")
csv_writer = csv.writer(csv_open)

# 스타벅스 음료 리스트 페이지 접속
driver = webdriver.Chrome()
driver.get(TARGET_URL_LIST)
driver.implicitly_wait(IMPLICIT_WAIT)

# 음료 제품 번호 가져오기
go_drink_views  = driver.find_elements_by_class_name('goDrinkView')
product_numbers = [a.get_attribute('prod') for a in go_drink_views]

for product_number in product_numbers:
    driver.get(TARGET_URL_DETAIL + product_number)

    # 한글 이름, 영어 이름
    name_kr, name_en = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/h4').text.split('\n')
    
    # 음료 설명
    description1_text = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/p').text.split('\n')
    description2_text = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]').text.split('\n')
    description1      = ' '.join(description1_text)
    description2      = ' '.join(description2_text)
    descriptions = []
    if description1 == description2:
        descriptions.append(description1)
    else:
        descriptions.append(description1)
        descriptions.append(description2)

    # 사이즈
    size_text    = driver.find_element_by_xpath('//*[@id="product_info01"]').text
    size_list    = re.sub('[^\w]|ml|fl|oz', ' ', size_text).split()
    size_name_en = ""
    size_name_kr = ""
    milliliter   = 0
    fluid_ounce  = 0 

    if len(size_list) == 4:          # 영어 이름, 한글 이름, 밀리리터, 액량 온스
        size_name_en = size_list[0]
        size_name_kr = size_list[1]
        milliliter   = size_list[2]
        fluid_ounce  = size_list[3]
    elif len(size_list) == 1:        # 밀리리터
        size_name_kr = "병"
        size_name_en = "Bottle"
        milliliter   = size_list[0]
    
    size = [size_name_en, size_name_kr, milliliter, fluid_ounce]

    # 영양 정보
    calorie       = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[2]/ul[1]/li[1]/dl/dd').text
    saturated_fat = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[2]/ul[1]/li[2]/dl/dd').text
    protein       = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[2]/ul[1]/li[3]/dl/dd').text
    sodium        = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[2]/ul[2]/li[1]/dl/dd').text
    sugar         = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[2]/ul[2]/li[2]/dl/dd').text
    caffeine      = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[2]/ul[2]/li[3]/dl/dd').text
    nutrition     = [calorie, saturated_fat, protein, sodium, sugar, caffeine]

    # 알레르기 유발 요인
    allergen_text = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/form/fieldset/div/div[3]/p').text
    allergens     = re.sub('[^\w]|알레르기 유발요인', ' ', allergen_text).split()
    
    # 이미지 URL
    image_urls = []
    images     = driver.find_elements_by_css_selector('#product_thum_wrap > ul > li > a > img')
    for image in images:
        image_urls.append(image.get_attribute('src'))

    # 카테고리
    category = driver.find_element_by_xpath('//*[@id="container"]/div[1]/div/ul/li[7]/a').text

    # csv 파일 저장
    row = (product_number, name_kr, name_en, category, descriptions, size, nutrition, allergens, image_urls)
    csv_writer.writerow(row)

    # CPU 쉬는 시간
    time.sleep(TIME_SLEEP)

# 리소스 종료
csv_open.close()
driver.quit()