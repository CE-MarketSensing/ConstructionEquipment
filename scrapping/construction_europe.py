import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 창 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)

# Navigate to the website
url = "https://www.construction-europe.com/8788.more"
driver.get(url)

# Click the cookie button
driver.find_element(By.CSS_SELECTOR, '#cookieConsent > div > div > div > div.col-12.col-md-auto.text-center.py-2.align-self-center > button').click()

req = urllib.request.Request(url)
sourcecode = urllib.request.urlopen(url).read()
soup = BeautifulSoup(sourcecode, "html.parser")

article_list = []
for href in soup.find_all("div", class_="khl-article-block-headline font-weight-bold h4"):
    address = href.find("a")["href"]
    full_address = "https://www.construction-europe.com" + address
    article_list.append(full_address)
    
print(article_list)

article_data = []
for article_link in article_list:
    driver.get(article_link)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    title = ""
    content = ""

    # 기사 제목 찾기
    title_elem = soup.find("h1", class_="khl-article-page-title")
    if title_elem:
        title = title_elem.get_text(strip=True)

    # 기사 내용 찾기
    content_elem = soup.find("div", class_="col-12 khl-article-page-storybody")
    if content_elem:
        paragraphs = content_elem.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

    article_data.append({"Title": title, "Content": content})

driver.quit()

df = pd.DataFrame(article_data)
print(df)

df.to_csv("construction_europe.csv", index=True)