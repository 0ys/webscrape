import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pymysql
import time
import sys

class Scraper:

    def __init__(self):
        self.jobs_db = [""]
        self.soup = None
    
    def get_data(self):
        return self.jobs_db
    
    def get_soup(self, url):
        print(f"Scraping {url}...", end=" ")
        response = requests.get(url)
        print(response.status_code)
        self.soup = BeautifulSoup(response.content, "html.parser")
    
    def scrape_page(self, url, keyword):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=True)
        print("Browsing..")
        page = browser.new_page()
        page.goto(url)

        # 키워드 입력 후 검색
        page.locator("input#bidNm.w350.mw98p").fill(keyword)
        time.sleep(1)
        page.locator("div.button4").locator("a.btn_mdl").first.click()
        final_url = page.url
        time.sleep(2)

        count = 0
        button_state = True
        # pagination
        while(button_state):
            count +=1
            time.sleep(2)
            if page.locator("a.default", has_text="+ 더보기").is_hidden(): break
            page.locator("a.default", has_text="+ 더보기").click()

        p.stop()

        # 페이지별로 스크래핑
        for x in range(count):
            page_url = f"{final_url}&currentPageNo={x+1}"
            self.get_soup(page_url)

            jobs = self.soup.find("table", class_="table_list_tbidTbl table_list")
            self.jobs_db[0] += str(jobs)

def dbconnect():
    conn = pymysql.connect(host='', user='', password='', db='', charset='utf8')
    return conn

def insert_data(conn, site_url, keyword, scrap_result):
    cur = conn.cursor()
    sql = f"INSERT INTO tbsys_web_scrap (site_url, keyword, scrap_result) VALUES('{site_url}', '{keyword}', '{scrap_result}')"
    cur.execute(sql)
    conn.commit()

def main(keyword):
    scraper = Scraper()

    url = "https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do?bidSearchType=1"
    scraper.scrape_page(url, keyword=keyword)
    jobs = scraper.get_data()

    # print(jobs)
    # print(f"{len(jobs)} scrape")

    conn = dbconnect()
    print("Connect DB...")
    insert_data(conn, site_url=url, keyword=keyword, scrap_result=jobs[0])
    print("Insert DB..")
    
    conn.close()
    print("Finished DB..")


if __name__ == '__main__':
    main(sys.argv[1])