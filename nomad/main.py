from flask import Flask, render_template, request
# templates 라고 정확히 명명된 폴더를 찾는다(현재 파일과 같은 위치에 있어야함)
from Scraper import Scraper

user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"

app = Flask("Scrapper")

@app.route("/") # decorator: 함수 바로 위에 위치해야함 "/"에 유저가 방문할 때 아래 함수를 실행하게 가리킴
def home():
    return render_template("home.html", name="ysgong") # rendering: flask는 주어진 변수를 모두 replace하면서 이 템플릿을 렌더링함

@app.route("/search")
def hello():
    skill = request.args.get("keyword")
    url = f"https://berlinstartupjobs.com/skill-areas/{skill}/"
    skill_scraper = Scraper(url, user)
    skill_scraper.scrape_page()
    # skill_scraper.save_data(f"jobs_{skill}.csv")
    jobs = skill_scraper.get_data()
    return render_template("search.html", keyword=skill, jobs=jobs)



app.run()


# url = "https://berlinstartupjobs.com/engineering/"
# page_scraper = Scraper(url, user)

# total_pages = page_scraper.get_pages()

# for x in range(total_pages):
#     url = f"https://berlinstartupjobs.com/engineering/page/{x+1}/"
#     scraper = Scraper(url, user)
#     scraper.scrape_page()
#     scraper.save_data(f"jobs_engineering.csv")