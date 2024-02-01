import threading
import socket
import time
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from waitress import serve
from Backend.Scraper import MegapersonalsScraper, SkipthegamesScraper, YesbackpageScraper, EscortalligatorScraper, \
    ErosScraper

# pyinstaller app.py --onefile --name=NetSpiderServer --hidden-import pyimod02_importers

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


class ScraperManager:
    def __init__(self):
        self.scraper_thread = None

    def start_scraper(self, kwargs):
        if self.scraper_thread is None or not self.scraper_thread.is_alive():
            self.scraper_thread = ScraperThread(kwargs)
            self.scraper_thread.start()
            self.scraper_thread.join()
            print("starting thread: ", threading.main_thread())
            return {"Response": "Scraper Thread Started"}
        else:
            return {"Response": "Scraper Thread is already running"}

    def manage_stop_scraper(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            self.scraper_thread.stop_thread()
            self.scraper_thread.join_with_timeout()  # Wait for the thread to finish
            print("thread count after stop: ", threading.active_count())
            return {"Response": "Scraper Thread Stopped Forcefully"}
        else:
            print("number of threads: ", threading.active_count())
            return {"Response": "No active Scraper Thread, Forceful Stop Attempted"}

    def get_scraper_status(self):
        print("scraper alive", self.scraper_thread.is_alive())
        print("scraper thread id:", self.scraper_thread.get_native_id())
        if self.scraper_thread and self.scraper_thread.is_alive():
            socketio.emit('scraper_update', {'status': 'scraper thread alive'})
        else:
            socketio.emit('scraper_update', {'status': 'scraper thread not alive'})


class ScraperThread(threading.Thread):
    def __init__(self, kwargs):
        keywords = set(kwargs['keywords'].split(','))
        flagged_keywords = set(kwargs['flagged_keywords'].split(','))
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
        self.scraper.set_keywords(keywords)
        print("keywords", keywords)
        print("scraper keywords", self.scraper.keywords)
        self.scraper.set_path(kwargs['path'])
        self.scraper.set_flagged_keywords(flagged_keywords)
        if kwargs['inclusive_search']:
            self.scraper.set_join_keywords()
        self.scraper.set_search_mode(kwargs['search_mode'])
        if kwargs['search_text'] != '':
            self.scraper.keywords.add(kwargs['search_text'])
        self.scraper.set_city(kwargs['city'])
        self._stop_event = threading.Event()

    def run(self):
        print("number of threads before: ", threading.active_count())
        while not self._stop_event.is_set() and not self.scraper.completed:
            thread_id = threading.get_native_id()
            print("scraper thread id", thread_id)
            global threads
            threads.add(threading.get_native_id())
            print(threads)
            socketio.emit('scraper_update', {'status': 'running'})
            print("right before run:", self.scraper.keywords)
            self.scraper.initialize()
            print(self.is_alive(), "1")
        print(self.scraper.completed, "scraper completed")
        print("thread id after close", threading.get_native_id())
        print("current thread  ", threading.current_thread())
        print(self.is_alive(), "thread is alive")
        if self.scraper.completed:
            print("scraper done")
            self.stop_thread()
            print("stopping thread")
            print(threading.current_thread().is_alive(), "2")
            print("id", threading.get_native_id())
            print("current thread  ", threading.current_thread())
        socketio.emit('scraper_update', {'status': 'completed'})

    def stop_thread(self):
        if not self.scraper.completed:
            self.scraper.stop_scraper()
        self._stop_event.set()

    def join_with_timeout(self, timeout=10):
        if not self.scraper.completed:
            print("join attempt in function")
            self.join(timeout)
            print("after join")
            if self.is_alive():
                print("Warning: ScraperThread did not terminate in time.")
        else:
            print("scraper is completed not joining")

    def stopped(self):
        return self._stop_event.is_set()


scraper_manager = ScraperManager()


def find_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    # os.environ['NETSPIDER_PORT'] = str(port)
    return port


@socketio.on('connection')
def connected():
    print("connected")


@socketio.on('scraper_status')
def get_status():
    scraper_manager.get_scraper_status()


@socketio.on('start_scraper')
def start_scraper(data):
    socketio.emit('scraper_update', {'status': 'started'})
    response = scraper_manager.start_scraper(data)
    return {'Response': response}


@socketio.on('stop_scraper')
def stop_scraper():
    response = scraper_manager.manage_stop_scraper()
    socketio.emit('scraper_update', {'status': 'stopped'})
    return {'Response': response}


@socketio.on_error('scraper_error')
def handle_error(e):
    print(f"An error occurred: {str(e)}")
    response = {"error": str(e)}
    return response, 500


if __name__ == "__main__":
    # start server
    # serve(app, host='127.0.0.1', port=5000)
    print("active threads: ", threading.active_count())
    open_port = find_open_port()
    socketio.run(app, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
