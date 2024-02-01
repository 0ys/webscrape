from flask import Flask, render_template
# templates 라고 정확히 명명된 폴더를 찾는다(현재 파일과 같은 위치에 있어야함)

app = Flask("Scrapper")

@app.route("/") # decorator: 함수 바로 위에 위치해야함 "/"에 유저가 방문할 때 아래 함수를 실행하게 가리킴
def home():
    return render_template("home.html", name="ysgong") # rendering: flask는 주어진 변수를 모두 replace하면서 이 템플릿을 렌더링함

@app.route("/search")
def hello():
    return render_template("search.html")

app.run()