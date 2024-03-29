from flask import Flask, render_template, request, redirect, send_file
from extractors.remoteok import get_jobs
from file import save_to_file

app = Flask("jobscrapper")
db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None or keyword =="":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        data = get_jobs(keyword)
        db[keyword] = data
    
    return render_template("search.html", keyword = keyword, jobs = data)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")