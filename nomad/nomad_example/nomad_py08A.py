'''
Build a scrapper for the berlinstartupjobs.com website.
Your scrapper should be able to scrape the following URLs:

https://berlinstartupjobs.com/engineering/ 
https://berlinstartupjobs.com/skill-areas/python/ 
https://berlinstartupjobs.com/skill-areas/typescript/ 
https://berlinstartupjobs.com/skill-areas/javascript/

The first URL has pages, so you will need to handle pagination.
The rest of the URLs are for specific skills, the structure of the URL has the skill name, so build a scrapper that can scrape any skill.
Extract the name of the company, the title of the job, the description and the link to the job.
'''

import requests
from bs4 import BeautifulSoup
import csv

class Scraper:

    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent
        self.jobs_db = []

    def scrape_page(self):
        print(f"Scraping {self.url}...", end=" ")
        response = requests.get(self.url, 
            headers={
            "User-Agent": self.user_agent
        })
        print(response.status_code)

        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find("ul", class_="jobs-list-items").find_all("li", class_="bjs-jlid")

        for job in jobs:
            title = job.h4.text
            company = job.find("a", class_="bjs-jlid__b").text
            description = job.find("div", class_="bjs-jlid__description").text
            link = job.find("a")["href"]

            job_data = {
                "title": title,
                "company": company,
                "description": description,
                "link": link,
            }
            self.jobs_db.append(job_data)

    def get_pages(self):
        response = requests.get(self.url, 
        headers={
        "User-Agent": self.user_agent
        })
        soup = BeautifulSoup(response.content, "html.parser")
        return len(soup.find("div", class_="bsj-template__b").find("ul", class_="bsj-nav").find_all("a"))

    def save_data(self, name):
        file = open(name, mode="w", encoding="utf-8", newline="")
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Description", "Link"])

        for job in self.jobs_db:
            writer.writerow(job.values())
        file.close()




user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"

url = "https://berlinstartupjobs.com/engineering/"
page_scraper = Scraper(url, user)

total_pages = page_scraper.get_pages()

for x in range(total_pages):
    url = f"https://berlinstartupjobs.com/engineering/page/{x+1}/"
    scraper = Scraper(url, user)
    scraper.scrape_page()
    scraper.save_data(f"jobs_engineering.csv")

skills = [
    "python",
    "typescript",
    "javascript",
    "rust"
]

for skill in skills:
    url = f"https://berlinstartupjobs.com/skill-areas/{skill}/"
    skill_scraper = Scraper(url, user)
    skill_scraper.scrape_page()
    skill_scraper.save_data(f"jobs_{skill}.csv")