'''
Using Flask, build a frontend for your job scraper.
The user should be able to search for a term, like python, javascript, java, etc.
The scraper should display results from berlinstartupjobs.com, weworkremotely.com and web3.career
We already have the code for the berlinstartupjobs.com scraper, you will need to write the code to scrape weworkremotely.com and web3.career
The search URLs are the following:
https://berlinstartupjobs.com/skill-areas// where <s> is the search term (i.e https://berlinstartupjobs.com/skill-areas/python/) 
https://web3.career/-jobs where <s> is the search term (i.e https://web3.career/python-jobs) 
https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term= where <s> is the search term (i.e https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python)
'''

from flask import Flask, render_template, request, redirect, send_file
import requests
from bs4 import BeautifulSoup
from Scraper import Scraper, Berlinstartupjobs, Web3, Weworkremotely
from file import save_to_file

user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"
app = Flask(__name__)

db = {}  # cache


@app.route("/")
def home():
    return render_template("home.html", name="ysgong")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        berlin_scraper = Berlinstartupjobs(user)
        berlin_url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
        berlin_scraper.scrape_page(berlin_url)
        berlin_jobs = berlin_scraper.get_data()

        web3_scraper = Web3(user)
        web3_url = f"https://web3.career/{keyword}-jobs"
        web3_scraper.scrape_page(web3_url)
        web3_jobs = web3_scraper.get_data()

        wework_scraper = Weworkremotely(user)
        wework_url = f"https://weworkremotely.com/remote-jobs/search?search_uuid=&term={keyword}"
        wework_scraper.scrape_page(wework_url)
        wework_jobs = wework_scraper.get_data()

        jobs = berlin_jobs + web3_jobs + wework_jobs
        db[keyword] = jobs
    print(db.keys())
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    jobs_db = db[keyword]

    file_name = f"jobs_{keyword}.csv"
    save_to_file(file_name, jobs_db)
    return send_file(file_name, as_attachment=True)


if __name__ == "__main__":
    app.run()
