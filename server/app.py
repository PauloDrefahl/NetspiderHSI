import gevent.monkey

import json

gevent.monkey.patch_all()

import threading
import socket
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from Backend.Scraper import MegapersonalsScraper, SkipthegamesScraper, YesbackpageScraper, EscortalligatorScraper, \
    ErosScraper, RubratingsScraper
from Backend.resultManager.appendResults import FolderAppender, FolderAppender
from Backend.resultManager.resultManager import ResultManager
from PyQt5.QtWidgets import QFileDialog, QApplication
from engineio.async_drivers import gevent
import subprocess
import sys
import os
import webbrowser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from apscheduler.schedulers.background import BackgroundScheduler

import time
import json
from datetime import datetime, timedelta
import schedule

app = Flask(__name__)
qt_app = QApplication([])
CORS(app)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

'''
    ---------------------------------
    Manage Scraper and threads
    ---------------------------------
'''


class DirectoryWatchHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Event triggered: {event}")  # Debugging line
        print("Updating files list...")  # Debugging line
        resultManager.update_folders_json()
        # resultList = resultManager.get_folders()
        #
        # # Check if resultList is not empty and send the list
        # if resultList:
        #     socketio.emit('result_folder_selected', {'folders': resultList})
        # else:
        #     # Notify if the directory is empty or there are no folders
        #     socketio.emit('result_folder_selected', {'error': 'No folders found in the selected directory'})

def list_threads():
    threads = threading.enumerate()
    for thread in threads:
        print(f"Thread Name: {thread.name}, Thread ID: {thread.ident}")

    return len(threads)



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

    def manage_stop_scraper(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            self.scraper_thread.stop_thread()
            self.scraper_thread.join_with_timeout()  # Wait for the thread to finish
            # thread_id = threading.get_native_id()
            print("thread count after stop: ", list_threads())
            return {"Response": "Scraper Thread Stopped Forcefully"}
        else:
            print("number of threads: ", list_threads())
            return {"Response": "No active Scraper Thread, Forceful Stop Attempted"}

    def get_scraper_status(self):
        print("get_scraper_status = ", self.scraper_thread.is_alive())
        if self.scraper_thread and self.scraper_thread.is_alive():
            socketio.emit('scraper_update', {'status': 'scraper thread alive'})
        else:
            socketio.emit('scraper_update', {'status': 'scraper thread not alive'})


class ScraperThread(threading.Thread):
    def __init__(self, kwargs):
        super().__init__()
        keywords = set(kwargs["keywords"])
        flagged_keywords = set(kwargs["flagged_keywords"])
        # Ignore empty search text.
        if kwargs["search_text"] != "":
            keywords.add(kwargs["search_text"])
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
        elif kwargs['website'] == 'rubratings':
            self.scraper = RubratingsScraper()
        self.scraper.set_keywords(keywords)
        self.scraper.set_path(kwargs['path'])
        self.scraper.set_flagged_keywords(flagged_keywords)
        if kwargs['inclusive_search']:
            self.scraper.set_join_keywords()
        self.scraper.set_search_mode(kwargs['search_mode'])
        if kwargs['payment_methods_only']:
            self.scraper.set_only_posts_with_payment_methods()
        self.scraper.set_city(kwargs['city'])
        self._stop_event = threading.Event()

    def run(self):
        print("number of threads before: ", list_threads())
        while not self._stop_event.is_set() and not self.scraper.completed:
            thread_id = threading.get_native_id()
            print("start thread id", thread_id)
            socketio.emit('scraper_update', {'status': 'running'})
            self.scraper.initialize()
            print(self.is_alive(), "1")
        print(self.scraper.completed, "scraper completed")
        print(self.is_alive(), "thread is alive")
        if self.scraper.completed:
            print("scraper done")
            self.stop_thread()
            print("stopping thread")
            # self.join_with_timeout()
            print(self.is_alive(), "2")
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


# Defining Scraper Manager Obj for managing scraper and its thread
scraper_manager = ScraperManager()

'''
    ---------------------------------
    Result Manager functions
    ---------------------------------   
'''


def initialize_result_manager(result_dir):
    # Access the stored result directory from Flask app configuration
    # result_dir = app.config.get('RESULT_DIR', 'default_directory_if_not_set')
    #print("stored result directory", result_dir)
    global resultManager
    resultManager = ResultManager(result_dir)
    resultManager.debug_print()

def initialize_folder_appender(result_dir):
    # Access the stored result directory from Flask app configuration
    # result_dir = app.config.get('RESULT_DIR', 'default_directory_if_not_set')
    #print("stored result directory", result_dir)
    global folderAppend
    folderAppend = FolderAppender(result_dir)


'''
    ---------------------------------
    Socket Routes
    ---------------------------------
'''


# Connection Manager Sockets
@socketio.on('connection')
def connected():
    print("connected")


# Scraper Manager Sockets
@socketio.on('scraper_status')
def get_status():
    scraper_manager.get_scraper_status()


@socketio.on('start_scraper')
def start_scraper(data):
    socketio.emit('scraper_update', {'status': 'started'})
    print(data)
    response = scraper_manager.start_scraper(data)
    return {'Response': response}


@socketio.on('stop_scraper')
def stop_scraper():
    response = scraper_manager.manage_stop_scraper()
    socketio.emit('scraper_update', {'status': 'stopped'})
    return {'Response': response}


# Result Manager Sockets
@socketio.on('start_append')
def start_append(data):
    print(data)
    socketio.emit('result_manager_update', {'status': 'appending'})
    folderAppend.setSelectedFolders(data)
    folderAppend.create_new_folder()
    folderAppend.append_files()
    folderAppend.save_data()
    response = 0
    return {'Response': response}


@socketio.on('open_PDF')
def open_PDF(data):
    socketio.emit('result_manager_update', {'status': 'view_pdf'})
    print(data)
    response = resultManager.view_pdf(data)
    return {'Response': response}


@socketio.on('open_ss_dir')
def open_ss_dir(data):
    socketio.emit('result_manager_update', {'status': 'view_SS_dir'})
    print(data)
    response = resultManager.view_ss_dir(data)
    return {'Response': response}


@socketio.on('open_clean_data')
def open_clean_data(data):
    socketio.emit('result_manager_update', {'status': 'view_clean_data'})
    print(data)
    response = resultManager.view_clean_data(data)
    return {'Response': response}


@socketio.on('open_raw_data')
def open_raw_data(data):
    socketio.emit('result_manager_update', {'status': 'view_raw_data'})
    print(data)
    response = resultManager.view_raw_data(data)
    print(response)
    return {'Response': response}


@socketio.on('open_diagram_dir')
def open_diagram_dir(data):
    socketio.emit('result_manager_update', {'status': 'view_diagram_dir'})
    print(data)
    response = resultManager.view_diagram_dir(data)
    return {'Response': response}


@socketio.on('set_result_dir')
def set_result_dir():
    print("Selecting result directory")
    directory = QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
    print("Selected Directory: ", directory)

    print("Selected Directory: ", directory)
    result_dir = os.path.join(os.getcwd(), directory)

    # initialize the folder appender and result manager
    initialize_result_manager(result_dir)
    initialize_folder_appender(result_dir)

    # get the result list from result manager
    resultList = resultManager.get_folders()

    print(resultList)

    print("sending Result list")
    socketio.emit('result_folder_selected', {'folders': resultList, 'result_dir': result_dir})


@socketio.on('refresh_result_list')
def refresh_result_list():

    resultManager.update_folders_json()

    resultList = resultManager.get_folders()

    # Check if resultList is not empty and send the list
    if resultList:
        socketio.emit('result_list_refreshed', {'folders': resultList})
    else:
        # Notify if the directory is empty or there are no folders
        socketio.emit('result_list_refreshed', {'error': 'No folders found in the selected directory'})

@socketio.on_error_default
def handle_error(e):
    print(f"An error occurred: {str(e)}")
    socketio.emit('scraper_update', {'status': 'error', 'error': str(e)})
    response = {"error": str(e)}
    return response, 500




#---------------------------------Auto Scraper---------------------------------
#Example data
# {
#     "Test": {
#       "data": {
#         "website": "escortalligator",
#         "city": "daytona",
#         "keywords": "",
#         "flagged_keywords": "",
#         "search_mode": false,
#         "search_text": "",
#         "payment_methods_only": false,
#         "inclusive_search": false,
#         "path": "result"
#       },
#       "frequency": "daily",
#       "duration": 5,
#       "last_run": "none"
#     }
#   }


#------function that will be called if the schedule is due------
def process_scraper(item_name, item_data):

    print(f"Processing {item_name}")
    #start the scraper with the given data, handled the same way as if the user clicked start from the site. 
    start_scraper(item_data['data'])
    



#------function that will run if the schedule is due------
def run_scheduled_scrapers():

    file_path = "server/scheduled_scrapers.json" #need to add the path to the file
    #if the file is not found (has been deleted), error out without crashing
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found. Ensure the file exists.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")

    print("Checking for scrapers to run...")

    for item_name, item_data in config.items():

        last_run = item_data['last_run']
        frequency = item_data['frequency']

        if last_run == "None":
            print(f"{item_name} has not run yet. Running now.")

            last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            config["Test"]["last_run"] = last_run  # Example new value
            print(config)
            with open(file_path, 'w') as json_file:
                json.dump(config, json_file, indent=4)

            process_scraper(item_name, item_data)

        
        else:

            last_run_date = datetime.strptime(last_run, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()

            if frequency == "daily" and now - last_run_date >= timedelta(days=1):
                print(f"{item_name} is scheduled for daily run. Running now.")
                process_scraper(item_name, item_data)

                last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                config["Test"]["last_run"] = last_run  # Example new value
                print(config)
                with open(file_path, 'w') as json_file:
                    json.dump(config, json_file, indent=4)

                process_scraper(item_name, item_data)
                

            elif frequency == "weekly" and now - last_run_date >= timedelta(weeks=1):
                print(f"{item_name} is scheduled for weekly run. Running now.")
                process_scraper(item_name, item_data)

                last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                config["Test"]["last_run"] = last_run  # Example new value
                print(config)
                with open(file_path, 'w') as json_file:
                    json.dump(config, json_file, indent=4)

                process_scraper(item_name, item_data)

            else:
                print(f"{item_name} is not due to run yet.")


#------End of Auto Scraper------

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(run_scheduled_scrapers, 'cron', hour=2, minute=00) 
scheduler.start()




'''
    ---------------------------------
    Finding ports
    ---------------------------------
'''


def write_open_ports(ports):
    with open('open_ports.txt', 'w') as file:
        for port in ports:
            file.write(str(port) + '\n')


def find_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def find_open_ports(num):
    open_ports_list = []
    for _ in range(num):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            open_ports_list.append(s.getsockname()[1])
    return open_ports_list


if __name__ == "__main__":
    print("active threads: ", list_threads())

    num_ports = 1  # Change this to the desired number of open ports
    open_ports = find_open_ports(num_ports)

    write_open_ports(open_ports)

    print("Open Ports:", open_ports)

    # Use the open ports as needed in the rest of your program
    # Note: You may want to handle the case where `open_ports` is an empty list.
    socketio.run(app, host='127.0.0.1', port=open_ports[0], allow_unsafe_werkzeug=True)
    
