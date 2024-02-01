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

    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.jobs_db = []

    def scrape_page(self, url):
        print(f"Scraping {url}...", end=" ")
        response = requests.get(url, 
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

    def get_pages(self, url):
        response = requests.get(url, 
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

    def get_data(self):
        return self.jobs_db
