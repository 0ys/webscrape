import requests
from bs4 import BeautifulSoup

all_jobs = []

def scrape_page(url):
    print(f"Scraping {url}...", end=" ")
    response = requests.get(url, 
        headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"
    })
    print(response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("table", id="jobsboard").find_all("tr", class_="job")

    for job in jobs:
        title = job.find("h2").text
        company = job["data-company"]
        extra_info = job.find("td", class_="company position company_and_position").find_all("div", class_="location")
        try:
            if len(extra_info) == 2:
                region, salary = extra_info 
            elif len(extra_info) == 3:
                region, salary, ohters = extra_info 
            else:
                region, *others, salary = extra_info
        except ValueError as e:
            print(e)
        
        
        job_info = job["data-href"] 

        job_data = {
            "title": title,
            "company": company,
            # "position": position.text,
            "region": region.text,
            "salary": salary.text,
            "job_info": f"https://remoteok.com{job_info}",
        }
        all_jobs.append(job_data)


keywords = [
    "flutter",
    "python",
    "golang"
]

for keyword in keywords:
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    scrape_page(url)

print(all_jobs)
print(len(all_jobs))