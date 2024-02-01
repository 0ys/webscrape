import requests
from bs4 import BeautifulSoup

all_jobs = []

def scrape_page(url):
    print(f"Scraping {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("section", class_="jobs").find_all("li")[1:-1] # 첫번째와 마지막 li는 필요없으므로 제거해줌

    for job in jobs:
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company") # html에 (귀찮아서) company라고 적힌 span들을 제대로 분류해줌
        
        job_info = job.find("div", class_="tooltip").next_sibling["href"] # 적절한 url 위치를 찾아서 가져옴, ["href"]를 호출하기 전 None 검사필요

        job_data = {
            "title": title,
            "company": company.text,
            "position": position.text,
            "region": region.text,
            "job_info": f"https://weworkremotely.com{job_info}",
        }
        all_jobs.append(job_data)

def get_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return len(soup.find("div", class_="pagination").find_all("span", class_="page"))


total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs")

for x in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

print(all_jobs)