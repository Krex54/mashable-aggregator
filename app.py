from flask import Flask, render_template
from scraper import scrape_mashable
import threading
import time

app = Flask(__name__)

cached_articles = []

# Load articles at startup
def load_articles():
    global cached_articles
    try:
        cached_articles = scrape_mashable()
    except Exception as e:
        print("Error loading articles:", e)

# Run the load once when the app starts
load_articles()

@app.route("/")
def index():
    return render_template("index.html", articles=cached_articles)

# Optional: update in the background every 15 minutes
def background_refresh():
    while True:
        load_articles()
        time.sleep(900)  # 15 minutes

# Start background refresh in a separate thread
threading.Thread(target=background_refresh, daemon=True).start()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
