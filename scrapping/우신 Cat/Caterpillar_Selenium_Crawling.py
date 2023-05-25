#!/usr/bin/env python
# coding: utf-8

# 
# # 오류가 나신다면 새로 켜진 창의 화면을 밑에 그림만큼 축소시켜보세요
# 
# ![nn](크롤링축소이미지.png)

# In[4]:


import pandas as pd
import time
import selenium
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service #chromedriver 자동설치
from webdriver_manager.chrome import ChromeDriverManager #chromedriver 자동설치
from selenium.webdriver.common.by import By #요소 찾을 때 사용
from selenium.webdriver.common.keys import Keys
service = Service(executable_path=ChromeDriverManager().install()) #크롬드라이버 설치
from selenium.webdriver import ActionChains

#인터넷 열어서 원하는 사이트 접속
driver = webdriver.Chrome(service=service)
driver.get("https://www.cat.com/en_US/news/machine-press-releases.html")

#쿠키 설정 들어가기
Cookie = driver.find_element(By.ID, 'onetrust-pc-btn-handler')
Cookie.click()

time.sleep(0.5)

#모두 거부
No = driver.find_element(By.CLASS_NAME, 'ot-pc-refuse-all-handler')
No.click()

#모두 동의
# Yes = driver.find_element(By.ID 'onetrust-accept-btn-handler')
# Yes.click()

#모두 동의를 원할시 쿠키 설정 들어가기에서부터 모두거부까지 주석 처리를 해주시고 모두 동의 부분 주석처리를 해제해주세요

time.sleep(1)

#기사내용 더보기
Load_more = driver.find_element(By.ID, "listID-0")

#총 페이지 수
page_total = driver.find_element(By.CLASS_NAME, "pagination--total")
pages = int(page_total.text)

#현재 보여지는 페이지 수 
page_current = driver.find_element(By.CLASS_NAME, "pagination--current")
page_currents = int(page_current.text)

#타임슬립을 너무 짧게 설정하면 다른 페이지로 넘어가요
for i in range(1,pages+1,25):
    try:
        Load_more.click()
        time.sleep(1)
    except:
        page_currents == pages
        
#기사 날짜와 제목 추출

DT = driver.find_element(By.ID, "container-1237bb0555")
DT = DT.text
DT = DT.split("\n")
del DT[0]

#날짜와 기사제목을 각각 Date,Title 리스트에 넣어줘요
Date=[]
Title=[]
Article = []

for i in range(1,101):
    #크롤링 하기 원하는 기사로 화면이동
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH ,f'//*[@id="container-1237bb0555"]/div/div/div/div/div/div[2]/div[1]/ul/li[{i}]')).perform()
    time.sleep(2)
    #기사 클릭
    driver.find_element(By.XPATH ,f'//*[@id="container-1237bb0555"]/div/div/div/div/div/div[2]/div[1]/ul/li[{i}]').click()
    #크롤링 except부분은 형식이 달라 따로 처리해요
    try:
        article = driver.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid > div > div:nth-child(8) > div').text
        article = article.split()
    except:
        article = driver.find_element(By.CLASS_NAME,"cmp-text").text
        article = article.split()
        del article[:3]
    time.sleep(1)
    try:
        if "Release" in article:
            r = article[:].index("Release",3)+3
            del article[:r]
    except:
        pass
    article = " ".join(article)
    Article.append(article)
    driver.back()
    time.sleep(2)
    #기사 25개 더보기 3번클릭 끝까지 출력하기를 염두함
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH ,'//*[@id="listID-0"]/span'))
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH ,'//*[@id="listID-0"]/span'))
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH ,'//*[@id="listID-0"]/span'))
    time.sleep(1)
    
for i in range(len(DT)):
    if i == 0 or i % 2 == 0:
        Date.append(DT[i])
    else:
        Title.append(DT[i])


#날짜, 기사제목 그리고 본문을 데이터프레임으로 만들기
df = {"Date" : Date, "Title" : Title, "Article" : Article}
df = pd.DataFrame(df)

     
#csv 파일로 추출해요
df.to_csv("Caterpillar.csv", index=False)

