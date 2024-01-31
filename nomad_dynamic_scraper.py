# > pip install playwright
# > playwright install

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)

page = browser.new_page()
page.goto("https://www.wanted.co.kr/search?query=python&tab=position")
# page.goto("https://www.wanted.co.kr/")
# time.sleep(4)

# page.click("button.Aside_searchButton__Xhqq3")
# time.sleep(4)

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")
# time.sleep(4)

# page.keyboard.down("Enter")
# time.sleep(5)

# page.click("a#search_tab_position")
# time.sleep(5)

for x in range(4):
    page.keyboard.down("End")
    time.sleep(5)

content = page.content()
p.stop()

soup = BeautifulSoup(content, "html.parser")
jobs = soup.find_all("div", class_="JobCard_container__FqChn")

jobs_db = []

for job in jobs:
    link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__ddkwM").text
    company = job.find("span", class_="JobCard_companyName__vZMqJ").text
    location = job.find("span", class_="JobCard_location__2EOr5").text
    reward = job.find("span", class_="JobCard_reward__sdyHn").text

    job = {
        "title": title,
        "company_name": company,
        "location": location,
        "reward": reward,
        "link": link,
    }
    jobs_db.append(job)

file = open("jobs.csv", mode="w", encoding="utf-8", newline="")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Location", "Reward", "Link"]) # list만 받음

for job in jobs_db:
    writer.writerow(job.values())

file.close()


