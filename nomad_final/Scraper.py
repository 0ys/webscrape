import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import re

PAGE_LIMIT = 5

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


class Berlinstartupjobs(Scraper):

    def __init__(self, user_agent):
        super().__init__(user_agent)

    # https://berlinstartupjobs.com/skill-areas/
    def scrape_page(self, url):
        super().scrape_page(url)
        jobs = self.soup.find(
            "ul", class_="jobs-list-items").find_all("li", class_="bjs-jlid")

        for job in jobs:
            title = job.h4.text
            company = job.find("a", class_="bjs-jlid__b").text
            # description = job.find("div", class_="bjs-jlid__description").text
            location = "Berlin"
            link = job.find("a")["href"]

            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "link": link,
            }
            self.jobs_db.append(job_data)


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
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto("https://web3.career/react-jobs?page=1")

        page_count = 0

        while(page.locator("a.page-link", has_text="Next").get_attribute("href")!="#"):
            if page_count >= PAGE_LIMIT: break
            page_count += 1
            time.sleep(2)
            page.locator("a.page-link", has_text="Next").click()
        
        content = page.content()
        p.stop()

        soup = BeautifulSoup(content, "html.parser")
        pages = soup.find("ul", class_="pagination").find("li", class_="page-item active").text

        return(int(pages))


class Weworkremotely(Scraper):

    def __init__(self, user_agent):
        super().__init__(user_agent)

    # https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python
    def scrape_page(self, url):
        super().scrape_page(url)

        job_sections = self.soup.find_all("section", class_="jobs")

        for section in job_sections:
            jobs = section.find_all("li")[:-1]

            # print(jobs)
            for job in jobs:
                title = job.find("span", class_="title").text
                company = job.find("span", class_="company").text
                location = job.find("span", class_="region company").text
                link = job.find(
                    "a", {'href': re.compile('/remote-jobs/*')})["href"]
                # link = job.find("div", class_="tooltip").next_siblings

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": f"https://weworkremotely.com/{link}",
                }
                self.jobs_db.append(job_data)
