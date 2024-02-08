import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

keyword = "상담"

class Scraper:

    def __init__(self):
        self.jobs_db = []
        self.soup = None
    
    def get_data(self):
        return self.jobs_db
    
    def get_soup(self, url):
        print(f"Scraping {url}...", end=" ")
        response = requests.get(url)
        print(response.status_code)
        self.soup = BeautifulSoup(response.content, "html.parser")
    
    def scrape_page(self, url):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=True)
        print("Browsing..")
        page = browser.new_page()
        page.goto(url)

        # 나라장터 메인화면에서 키워드 입력 및 검색
        page.locator("input#bidNm.w387").fill(keyword)
        time.sleep(2)

        page.click("a.btn_dark")
        time.sleep(2)
        print(f"Searching keywords:{keyword}")

        # 검색결과 테이블 url 찾기
        frame_url = page.frame_locator("#sub").get_by_title("콘텐츠프레임").get_attribute("src")
        p.stop()
        n = self.get_page_num(frame_url)
        
        # content = page.content()

        # soup = BeautifulSoup(content, "html.parser")
        # pages = soup.find("div", id="pagination").get_by_title("현재페이지").text

        for x in range(n):
            page_url = f"{frame_url}&currentPageNo={x+1}"
            self.get_soup(page_url)

            jobs = self.soup.find("table", class_="table_list_tbidTbl table_list")
            self.jobs_db.append(jobs)
    
    def get_page_num(self, url):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        
        count = 0
        # pagination
        while(page.get_by_text("검색된 데이터가 없습니다.")!=None):
            time.sleep(2)
            print(page.get_by_text("검색된 데이터가 없습니다."))
            count +=1
            page.locator("a.default", has_text="+ 더보기").click()
            print("page clicked")
        
        print(count)
        return count


scraper = Scraper()

url = "https://www.g2b.go.kr/index.jsp"
scraper.scrape_page(url)
jobs = scraper.get_data()

print(jobs)
print(len(jobs))