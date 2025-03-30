#standard library imports
import os
import json
import threading
from datetime import datetime, timedelta

#third-party imports
import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from PyQt5.QtWidgets import QFileDialog, QApplication
from engineio.async_drivers import gevent
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger


#local imports
from Backend.Scraper import (
    MegapersonalsScraper,
    SkipthegamesScraper,
    YesbackpageScraper,
    EscortalligatorScraper,
    ErosScraper,
    RubratingsScraper
)
from Backend.resultManager.appendResults import FolderAppender
from Backend.resultManager.resultManager import ResultManager

<<<<<<< HEAD
=======

>>>>>>> e233b9b (Refactor import statements for better organization and clarity)
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

    def wait_for_scraper_to_complete(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            print("Waiting for the scraper thread to finish...")
            self.scraper_thread.join()


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
@socketio.on("connect")
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




'''
    ---------------------------------
    Auto Scraper 
    ---------------------------------
'''

#---------------------------------Auto Scraper Prototype---------------------------------
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
#        "weekly": false,                       bool
#        "daily": true,                         bool
#       "runs_left": 1,                         int
#        "last_run": "2025-03-28 18:22:00",     string
#        "day_to_run": "",                      string(Mon, Tue, Wed, Thu, Fri, Sat, Sun)(recommend) or int(1-7 would be Monday to Sunday) 
#        "hour": "*",                           int
#        "minute": "*/1",                       int
#        "job_id": ""                           make empty string if user modifies json
#     }
#   }

# Info related to scraper 03/30/2025
# Was rebuilt using APSchedular 3.11.0.
# Need to add 
    # The time the scraper runs at (done)
    # Be able to scrap back in time
    # What if scraper with same name replace a scraper that is loaded (when user does this json must make job_id empty string)
    # What happens if the user deletes the scraper (done)
    # What happens if a scraper runs, while it is supposed to be deleted (scraper won't run if json as been modified but it is still scheduled)
    # What happens if the name gets changed but none of the data does (job_ id empty string needed)
    # If the scheduler restarts none of the jobs will be okay if they arent said in a job scheduler

#------function called to load automatic scrapers from json------
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"File {file_path} not found. Ensure the file exists.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")

#------function called to save scraper updates after run------
def save_json(config, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(config, json_file, indent=4)

def process_scraper(scraper_name, scraper_settings):
        print(f"Processing {scraper_name}")
        # Start the scraper
        start_scraper(scraper_settings['data'])
        # Wait for the scraper to complete
        scraper_manager.wait_for_scraper_to_complete()
        print(f"{scraper_name} processing complete.")

def load_autoscraper_jobs():
        # Gets autoscrapers configurations from json file
        file_path = "server/scheduled_scrapers.json"
        config = load_json(file_path)
        
        # Gives any schedule scraper 2 hours to start from start time before terminating and not running
        scraper_grace_period = 7200 # time in seconds
        
        print("Checking for autoscraper to load")

        for scraper_config_name, scraper_settings in config.items():

            run_weekly = scraper_settings["weekly"]
            run_daily  = scraper_settings["daily"]
            job_id = scraper_settings["job_id"]
            runs_left = scraper_settings["runs_left"]
            
            # If the scraper doesn't have a job id and needs to be ran
            if job_id == "" and runs_left > 0:
                if run_weekly:
                    weekly_cron_trigger = CronTrigger(day=scraper_settings["day_to_run"], hour=scraper_settings["hour"], minute=scraper_settings["minute"])
                    job_object = scheduler.add_job(run_scheduled_scraper, weekly_cron_trigger, misfire_grace_time= scraper_grace_period, args=[scraper_config_name, "scrap"] )
                    print(f"Scraper Loaded: {scraper_config_name}, Scraper ID: {job_object.id}")
                    config[scraper_config_name]["job_id"] = job_object.id
                    save_json(config, file_path)

                elif run_daily:
                    daily_cron_trigger = CronTrigger(hour=scraper_settings["hour"], minute=scraper_settings["minute"])
                    job_object = scheduler.add_job(run_scheduled_scraper, trigger=daily_cron_trigger, misfire_grace_time= scraper_grace_period, args=[scraper_config_name, "scrap"] )
                    print(f"Scraper Loaded: {scraper_config_name}, Scraper ID: {job_object.id}")
                    config[scraper_config_name]["job_id"] = job_object.id
                    save_json(config, file_path)

def delete_autoscraper_jobs():
    file_path = "server/scheduled_scrapers.json" 
    config = load_json(file_path)

    for scraper_config_name, scraper_settings in config.items():
        runs_left = scraper_settings["runs_left"]
        scraper_id = scraper_settings["job_id"]
        
        # Deletes job from scraper if it has no runs left
        if runs_left <= 0 and scraper_id != "":
            print("Deleting due to scraper finishing all runs")
            job_id = scraper_settings["job_id"]
            scheduler.remove_job(job_id)
            
            scraper_settings["job_id"] = ""
            scraper_settings["runs_left"] = 0
        
            save_json(config, file_path)

    # Deletes scrapers if they have be rename,deleted, modified
    current_schedules = scheduler.get_jobs()
    for job in current_schedules:
        job_id, scraper_args  = job.id, job.args
        # Only deleting the scraper
        # Need to check logic
        try: 
            if scraper_args[1] == "scrap":
                scraper_name = scraper_args[0]
                
                if scraper_name in config:
                    #Modified
                    # deleting from scheduler because the user has modified the exist scheduler's json
                    if job_id != config[scraper_name]["job_id"]:
                        print("Deleting due to scraper being data being modified by user")
                        scheduler.remove_job(job_id)
                # Rename/Deleted
                # Deleting from scheduler because the scraper in not in the json
                else:
                    print("Deleting due to scraper not being listed in json")
                    scheduler.remove_job(job_id)
        except:
            print("Job is not a scraper")

#################Task Section for ApScheduler#########################
#------function called to manage_scrapers------
# manage scraper is called by our scheduler at the start up
# it will delete scrapers if they are modified, delete, or renamed
# it will also assign new scrapers or reassign modified scraper to the scheduler
def manage_scraper():
    count = 0
    print("Before management:")
    for job in scheduler.get_jobs():
        count += 1
        print(f"{count})Job ID:{job.id}\n Job function: {job.func}\n Job argments: {job.args}\n")
    delete_autoscraper_jobs()
    load_autoscraper_jobs()
    count = 0
    print("After management:")
    for job in scheduler.get_jobs():
        count += 1
        print(f"{count})Job ID:{job.id}\n Job function: {job.func}\n Job argments: {job.args}\n")

#------function called to run scraper------
def run_scheduled_scraper(scraper_name, function_name):
    
    file_path = "server/scheduled_scrapers.json" 
    config = load_json(file_path)

    print(f"Checking for scraper: {scraper_name}\nTask:{function_name}")
    if scraper_name in config:
        print(f"Running Scraper:{scraper_name}")
        scraper_config = config[scraper_name]
        runs_left = scraper_config["runs_left"]

        # if a scraper was to run before getting deleted by the manager
        # The if statement would stop it
        if runs_left > 0:
            
            last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            scraper_config["last_run"] = last_run  # Updates last run time value
            scraper_config["runs_left"] -= 1  # Updates count of days/weeks left

            #Scraper does things
            print(f"Scraper running:{scraper_name}\n Last time scraper ran: {scraper_config['last_run']} \n Runs left:{scraper_config['runs_left']}\n Scraper Id:{scraper_config['job_id']}")
            process_scraper(scraper_name, scraper_config)
            
            print(f"Scraper Finished: {scraper_name}")
            save_json(config, file_path)  
    
# Start of main code
# Test for later(Will put process on multiple cpus):
#       -processpool: ProcessPoolExecutor(2)
#                     ThreadPoolExecutor(1)
executors = {
    # Assign to Background Scheduler so it only has 1 thread to use
    'default': ThreadPoolExecutor(1)
}

# declartion of background scheduler class
scheduler = BackgroundScheduler(executors=executors)

# Assign to manage_scheduler job
# "*/15"
manage_schedule_trigger = CronTrigger(minute="*/2")

# Adds manage_scraper job to the scheduler
# Triggers every 15 minutes
# Uses default executor
# misfire_grace_time = lets thread exist for 15 minutes without firing
# if two manage_scraper job exist in queue, coalesce will make it fire only once for multiple instances
scheduler.add_job(manage_scraper, manage_schedule_trigger, executor="default", misfire_grace_time=900, coalesce=True)

# start scheduler
scheduler.start()



<<<<<<< HEAD
=======
#-------------------------------Translator functions---------------------------------

#translate keywords function v0, current discussion topic is to move keywords/sets to a DB instead of a file.
#current state of this function is dormant, need to make changes to front end and determine keyword handling method for the future.

#2 - Function is called by socket.io translate and is passed language to translate the keywords file to
def translate_keywords(language):
    
    print("Opening keyword file")
    with open('keywords.txt', 'r') as file:
        keywords = file.read().splitlines()

    print("Calling Google Translate")

    translated_keywords = []

    #will need to restructure loop, goal will be to take list of english words and return translated list in following format:
    #original word 1, language 1 translated word 1, language 2 translated word 1, original word 2, language 1 translated word 2, language 2 translated word 2, etc.
    for word in keywords:
        if word.strip():
            safe_word = str(word) #if we go DB route, I imagine a lot of my error handling will be obsolete but TBD
            print(f"Translating: {safe_word}")
            translated_keywords.append(GoogleTranslator(source="auto", target=language).translate(safe_word))

    #print all translated words
    for translated_word in translated_keywords:
        print(translated_word)

    #translator works, gets all the keywords from the file and translates them. 


#1 - When translate button is hit on front end, this function is called and data is passed to it
@socketio.on('translator')
def translator(language):
    print(f"translate_keywords({language}) called...")
    translate_keywords(language)

#-------------------------------Translator End---------------------------------


>>>>>>> 5800dde (Init translator code, very early stage)
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

    socketio.run(app, host='127.0.0.1', port=5173, allow_unsafe_werkzeug=True)
    
