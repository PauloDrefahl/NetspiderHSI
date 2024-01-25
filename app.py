import threading
import time
from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from Backend.Scraper import MegapersonalsScraper, SkipthegamesScraper, YesbackpageScraper, EscortalligatorScraper, \
    ErosScraper

# pyinstaller app.py --onefile --name=NetSpiderServer --hidden-import pyimod02_importers

app = Flask(__name__)
CORS(app)


class ScraperManager:
    def __init__(self):
        self.scraper_thread = None

    def start_scraper(self, kwargs):
        if self.scraper_thread is None or not self.scraper_thread.is_alive():
            self.scraper_thread = ScraperThread(kwargs)
            self.scraper_thread.start()
            return {"Response": "Scraper Thread Started"}
        else:
            return {"Response": "Scraper Thread is already running"}

    def force_stop(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            self.scraper_thread.force_stop()
            self.scraper_thread.join_with_timeout()
            return {"Response": "Scraper Thread Force Stopped"}
        else:
            return {"Response": "No active Scraper Thread, Force Stop Attempted"}

    def stop_scraper(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            print("here 0")
            self.scraper_thread.stop()
            print("here attempting join")
            # self.scraper_thread.join_with_timeout()  # Wait for the thread to finish
            print("here 2")
            print("final thread", self.scraper_thread.is_alive())
            return {"Response": "Scraper Thread Stopped Gracefully"}
        else:
            return {"Response": "No active Scraper Thread, Graceful Stop Attempted"}


class ScraperThread(threading.Thread):
    def __init__(self, kwargs):
        super(ScraperThread, self).__init__()
        if kwargs['website'] == 'eros':
            self.scraper = ErosScraper()
        elif kwargs['website'] == 'escortalligator':
            self.scraper = EscortalligatorScraper()
        elif kwargs['website'] == 'megapersonals':
            self.scraper = MegapersonalsScraper()
        elif kwargs['website'] == 'skipthegames':
            self.scraper = SkipthegamesScraper()
        elif kwargs['website'] == 'yesbackpage':
            self.scraper = YesbackpageScraper()
        self.scraper.keywords = kwargs['keywords']
        self.scraper.set_path(kwargs['path'])
        self.scraper.set_flagged_keywords(kwargs['flagged_keywords'])
        if kwargs['inclusive_search']:
            self.scraper.set_join_keywords()
        self.scraper.set_search_mode(kwargs['search_mode'])
        self.scraper.keywords.add(kwargs['search_text'])
        self.scraper.set_city(kwargs['city'])
        # self.scraper.initialize(kwargs['keywords'])
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set() and not self.scraper.completed:
            self.scraper.initialize()
            print(self.is_alive(), "1")
        print(self.scraper.completed, "scraper completed")
        print(self.is_alive(), "thread is alive")
        if self.scraper.completed:
            print("scraper done")
            scraper_manager.stop_scraper()
            print(self.is_alive(), "2")

    def force_stop(self):
        self.scraper.stop_scraper()
        self._stop_event.set()

    def stop(self):
        self._stop_event.set()

    def join_with_timeout(self, timeout=1):
        print("join attempt in function")
        self.join(timeout)
        print("after join")
        if self.is_alive():
            print("Warning: ScraperThread did not terminate in time.")

        # if self.is_alive():
        #     self._stop_event.clear()

    def stopped(self):
        return self._stop_event.is_set()


scraper_manager = ScraperManager()


def get_params():
    return {
        "website": get_website(),
        "city": get_city(),
        "keywords": get_keywords(),
        "flagged_keywords": get_flagged_keywords(),
        "search_mode": get_search_mode(),
        "search_text": get_search_text(),
        "inclusive_search": get_inclusive_search(),
        "path": get_path(),
    }


def get_website():
    return request.args.get("website", default="yesbackpage", type=str).strip()


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


@app.route("/start_scraper")
def start_scraper():
    params = get_params()
    return scraper_manager.start_scraper(params)


@app.route("/stop_scraper")
def stop_scraper():
    print("stop scraper function")
    return scraper_manager.force_stop()


@app.errorhandler(Exception)
def handle_error(e):
    print(f"An error occurred: {str(e)}")
    response = {"error": str(e)}
    return response, 500


if __name__ == "__main__":
    # start server
    serve(app, host='127.0.0.1', port=5000)
