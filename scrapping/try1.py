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

article_data = []
# Scrape articles
while True:
    # Get page source and create BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Scrape article details
    for article in soup.find_all("div", class_="khl-article-block-headline font-weight-bold h4"):
        # Get article URL
        address = article.find("a")["href"]
        full_address = "https://www.construction-europe.com" + address
        # for _ in range(4):   
        #     next_page_button = driver.find_element(By.CSS_SELECTOR, '#CategoryPager > div > ul > li:nth-child(2) > a').click()
        # print(full_address)

    # Click the next page button
    next_page_button = driver.find_element(By.CSS_SELECTOR, '#CategoryPager > div > ul > li:nth-child(2) > a').click
    time.sleep(2)

        # Go to article page
        driver.get(full_address)
        time.sleep(2)
        article_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Scrape release date
        release_date_elem = article_soup.find("span", class_="PubDate")
        release_date = release_date_elem.text.strip() if release_date_elem else ""
        
        # Scrape news title
        title_elem = article_soup.find("h1", class_="khl-article-page-title")
        title = title_elem.text.strip() if title_elem else ""
                
        # Scrape article content
        content_elem = article_soup.find("div", class_="col-12 khl-article-page-storybody")
        paragraphs = content_elem.find_all("p") if content_elem else []
        content = "\n".join([p.text.strip() for p in paragraphs])
        
        # Append article data to the list
        article_data.append({"Release Date": release_date, "News Title": title, "Article Content": content})

    # Go to the next page
    try:
        next_page_button = driver.find_element(By.CSS_SELECTOR, '#CategoryPager > div > ul > li:nth-child(2) > a').click()
        # driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button) 
        # next_page_button.click()
        time.sleep(2)
    except:
        print("No more pages to scrape.")
        break

driver.quit()

# Create DataFrame from article data
df = pd.DataFrame(article_data)

# Save DataFrame to CSV
df.to_csv("construction2.csv", index=False)