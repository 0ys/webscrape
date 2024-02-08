import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import re

PAGE_LIMIT = 10

class Scraper:

    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.jobs_db = []
        self.soup = None

    def get_soup(self, url):
        print(f"Scraping {url}...", end=" ")
        response = requests.get(url,
                                headers={
                                    "User-Agent": self.user_agent
                                })
        print(response.status_code)
        self.soup = BeautifulSoup(response.content, "html.parser")
    
    def scrape_page(self, url):
        self.get_soup(url)
    
    def get_data(self):
        return self.jobs_db


class Web3(Scraper):

    def __init__(self, user_agent):
        super().__init__(user_agent)

    # https://web3.career/python-jobs
    def scrape_page(self, url):
        pages = self.get_pages(url)

        for x in range(pages): # pagination
            new_url = f"{url}?page={x+1}"
            super().scrape_page(new_url)

            jobs = self.soup.find("table", class_="table table-borderless").find_all("tr", class_="table_row")

            for job in jobs:
                if job.h2: title = job.h2.text
                if job.h3: company = job.h3.text
                location_a = job.find("a", style="font-size: 12px; color: #d5d3d3;")
                location_span = job.find("span", style="font-size: 12px; color: #d5d3d3;")
                if location_a: location = location_a.text
                if location_span: location = location_span.text
                link = job.find("a")["href"]

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": f"https://web3.career{link}",
                }
                self.jobs_db.append(job_data)
    
    def get_pages(self, url):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto("https://web3.career/react-jobs?page=1")

        page_count = 0

        while(page.locator("a.page-link", has_text="Next").get_attribute("href")!="#"):
            if page_count >= PAGE_LIMIT: break
            page_count += 1
            time.sleep(4)
            page.locator("a.page-link", has_text="Next").click()
        
        content = page.content()
        p.stop()

        soup = BeautifulSoup(content, "html.parser")
        pages = soup.find("ul", class_="pagination").find("li", class_="page-item active").text

        return(int(pages))



user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"
web3_scraper = Web3(user)
web3_url = f"https://web3.career/python-jobs"
web3_scraper.scrape_page(web3_url)
# web3_scraper.get_pages(web3_url)
web3_jobs = web3_scraper.get_data()

print(web3_jobs)