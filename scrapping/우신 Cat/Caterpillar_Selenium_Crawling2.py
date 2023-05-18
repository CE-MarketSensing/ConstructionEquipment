#!/usr/bin/env python
# coding: utf-8

# In[525]:


import pandas as pd
import time
import selenium
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service #chromedriver 자동설치
from webdriver_manager.chrome import ChromeDriverManager #chromedriver 자동설치
from selenium.webdriver.common.by import By #요소 찾을 때 사용
service = Service(executable_path=ChromeDriverManager().install()) #크롬드라이버 설치

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

time.sleep(0.5)

#기사내용 더보기
Load_more = driver.find_element(By.ID, "listID-0")

#총 페이지 수
page_total = driver.find_element(By.CLASS_NAME, "pagination--total")
pages = int(page_total.text)

#현재 보여지는 페이지 수 
page_current = driver.find_element(By.CLASS_NAME, "pagination--current")
page_currents = int(page_current.text)

# #타임슬립을 너무 짧게 설정하면 다른 페이지로 넘어가요
# for i in range(1,pages+1,25):
#     try:
#         Load_more.click()
#         time.sleep(1)
#     except:
#         page_currents == pages
        
# #기사 날짜와 제목 추출

# article = driver.find_element(By.ID, "container-1237bb0555")

# #기사 날짜와 제목을 리스트로 만들어줘요
# i=[]

# for news in article.text:
#     i.append(news)
# #띄어쓰기와 필요없는 첫줄을 제거해요    
# df_list = "".join(i).split("\n")
# del df_list[0]

# #딕셔너리로 바꿔줘요
# dictionary = {i : df_list[i] for i in range(len(df_list))}
# #날짜와 기사제목을 각각 a,b리스트에 넣어줘요
# a=[]
# b=[]

# for i in dictionary:
#     if i == 0 or i % 2 == 0:
#         a.append(dictionary[i])
#     else:
#         b.append(dictionary[i])
# #날짜와 기사제목을 시리즈로 만들고 데이터 프레임으로 만들고 데이터프레임을 표시해요.   
# a = pd.Series(a, index=None)
# b = pd.Series(b)
# df = pd.DataFrame(a)
# df.columns = ["Date"]
# df["Article"] = b        
# #csv 파일로 추출해요
# # df.to_csv("Caterpillar.csv", index=False)


# In[420]:


#총 페이지 수
page_total = driver.find_element(By.CLASS_NAME, "pagination--total")
pages = int(page_total.text)

#현재 보여지는 페이지 수 
page_current = driver.find_element(By.CLASS_NAME, "pagination--current")
page_currents = int(page_current.text)


# In[438]:


news_title = []
news_datetime = []
news_author = []
news_summary = []
news_article = []


# In[445]:


Load_more = driver.find_element(By.ID, "listID-0")

for i in range(1,26):
    driver.find_element(By.CSS_SELECTOR, f'#container-1237bb0555 > div > div > div > div > div > div.list__list-col > div.list__wrapper > ul > li:nth-child({i}) > a').click()
    article = driver.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid > div > div:nth-child(8) > div').text
    article = article.split()
    r = article[:].index("Release",3)+2
    del article[:r]
    article = " ".join(article)
    news_article.append(article)
    driver.find_element(By.CSS_SELECTOR, "body > div.root.responsivegrid > div > div.cmp-breadcrumb.aem-GridColumn.aem-GridColumn--default--12 > div > div > div > div > ul > li:nth-child(2) > a").click()
    time.sleep(0.5)


# In[517]:


# 기사 들어가기
driver.find_element(By.CSS_SELECTOR, f'#container-1237bb0555 > div > div > div > div > div > div.list__list-col > div.list__wrapper > ul > li:nth-child(10) > a').click()


# In[501]:


article = driver.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid > div > div:nth-child(8) > div').text
article = article.split()


# In[513]:


r = article[:].index("Release",3)+2


# In[523]:


r


# In[514]:


article[:r]


# In[518]:


article = driver.find_element(By.CSS_SELECTOR, 'body > div.root.responsivegrid > div > div:nth-child(8) > div').text
article = article.split()


# In[522]:


article[:].index("Release",3)
article[:10]


# In[516]:


#Machine Product & Service Announcements로 돌아가기
driver.find_element(By.CSS_SELECTOR, "body > div.root.responsivegrid > div > div.cmp-breadcrumb.aem-GridColumn.aem-GridColumn--default--12 > div > div > div > div > ul > li:nth-child(2) > a").click()


# In[126]:


#검색하는 돋보기 아이콘

first_sel = driver.find_element(By.ID, "utility_links_search_icon")

#돋보기 클릭하기
first_sel.click()

#검색창 클릭

second_sel = driver.find_element(By.ID, "searchInput")

#검색창에 데이터를 입력하기

second_sel.send_keys("우신짱2")

