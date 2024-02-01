from flask import Flask, render_template, request, redirect, send_file
# render_template: templates 라고 정확히 명명된 폴더를 찾는다(현재 파일과 같은 위치에 있어야함)
from Scraper import Scraper
from file import save_to_file

user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"

app = Flask("Scrapper")
scraper = Scraper(user)

db = {} # cache


@app.route("/") # decorator: 함수 바로 위에 위치해야함 "/"에 유저가 방문할 때 아래 함수를 실행하게 가리킴
def home():
    return render_template("home.html", name="ysgong") # rendering: flask는 주어진 변수를 모두 replace하면서 이 템플릿을 렌더링함

@app.route("/search")
def search():
    keyword = request.args.get("keyword") # url에 있는 keyword 정보를 가지고옴
    if keyword == None: return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else: 
        url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
        scraper.scrape_page(url)
        jobs = scraper.get_data()
        db[keyword] = jobs
    print(db.keys())
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None: return redirect("/")
    if keyword not in db: return redirect(f"/search?keyword={keyword}")
    scraper.save_data(f"jobs_{keyword}.csv")
    return send_file(f"jobs_{keyword}.csv", as_attachment=True)

app.run()