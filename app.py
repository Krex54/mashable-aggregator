from flask import Flask, render_template
from scraper import scrape_mashable

app = Flask(__name__)

@app.route("/")
def home():
    articles = scrape_mashable()
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
