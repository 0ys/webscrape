import requests
from bs4 import BeautifulSoup
import re


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
    
    def get_data(self):
        return self.jobs_db


class Weworkremotely(Scraper):

    def __init__(self, user_agent):
        super().__init__(user_agent)

    # https://weworkremotely.com/remote-jobs/search?search_uuid=&term=react
    def scrape_page(self, url):
        super().get_soup(url)

        job_sections = self.soup.find_all("section", class_="jobs")

        for section in job_sections:
            jobs = section.find_all("li")[:-1]

            # print(jobs)
            for job in jobs:
                title = job.find("span", class_="title").text
                company = job.find("span", class_="company").text
                location = job.find("span", class_="region company").text
                link = job.find("a", {'href':re.compile('/remote-jobs/*')})["href"]
                # link = job.find("div", class_="tooltip").next_siblings

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": f"https://weworkremotely.com/{link}",
                }
                self.jobs_db.append(job_data)

user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"
wework_scraper = Weworkremotely(user)
wework_url = f"https://weworkremotely.com/remote-jobs/search?search_uuid=&term=react"
wework_scraper.scrape_page(wework_url)
wework_jobs = wework_scraper.get_data()

print(wework_jobs)