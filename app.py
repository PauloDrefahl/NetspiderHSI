import psutil
from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from Backend.Scraper import MegapersonalsScraper, SkipthegamesScraper, YesbackpageScraper, EscortalligatorScraper, \
    ErosScraper

# pyinstaller app.py --onefile --name=NetSpiderServer --hidden-import pyimod02_importers

app = Flask(__name__)
CORS(app)


def get_params():
    return {
        "city": get_city(),
        "keywords": get_keywords(),
        "flagged_keywords": get_flagged_keywords(),
        "search_mode": get_search_mode(),
        "search_text": get_search_text(),
        "inclusive_search": get_inclusive_search(),
        "path": get_path(),
    }


def get_path():
    return request.args.get("path", default='C:\\Users\\Zach\\PycharmProjects\\flaskTest\\result', type=str).strip()


def get_inclusive_search():
    return request.args.get("inclusive_search", default=False, type=bool)


def get_search_text():
    return request.args.get("search_text", default="", type=str).strip()


def get_search_mode():
    return request.args.get("search_mode", default=False, type=bool)


def get_flagged_keywords():
    flagged_keywords_str = request.args.get("flagged_keywords", default="", type=str).strip()
    return set(flagged_keywords_str.split(',')) if flagged_keywords_str else set()


def get_city():
    return request.args.get("city", type=str).strip()


def get_keywords():
    keywords_str = request.args.get("keywords", default="", type=str).strip()
    return set(keywords_str.split(',')) if keywords_str else set()


def run_scraper(scraper_class, **kwargs):
    scraper = scraper_class()
    scraper.set_path(kwargs['path'])
    print(scraper.path)
    scraper.set_flagged_keywords(kwargs['flagged_keywords'])
    if kwargs['inclusive_search']:
        scraper.set_join_keywords()
    scraper.set_search_mode(kwargs['search_mode'])
    scraper.keywords.add(kwargs['search_text'])
    scraper.set_city(kwargs['city'])
    scraper.initialize(kwargs['keywords'])
    return {"Response": "Scraper Start"}


@app.route("/eros_scraper")
def eros_scraper():
    params = get_params()
    return run_scraper(ErosScraper, **params)


@app.route("/escortalligator_scraper")
def escortalligator_scraper():
    params = get_params()
    return run_scraper(EscortalligatorScraper, **params)


@app.route("/megapersonals_scraper")
def megapersonals_scraper():
    params = get_params()
    return run_scraper(MegapersonalsScraper, **params)


@app.route("/skipthegames_scraper")
def skipthegames_scraper():
    params = get_params()
    return run_scraper(SkipthegamesScraper, **params)


@app.route("/yesbackpage_scraper")
def yesbackpage_scraper():
    params = get_params()
    return run_scraper(YesbackpageScraper, **params)


@app.errorhandler(Exception)
def handle_error(e):
    print(f"An error occurred: {str(e)}")
    response = {"error": str(e)}
    return response, 500


if __name__ == "__main__":
    # start server
    serve(app, host='127.0.0.1', port=5000)
