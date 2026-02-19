# We should patch the standard library as early as possible.
# Source: https://www.gevent.org/api/gevent.monkey.html
# ruff: noqa: E402
import gevent.monkey

gevent.monkey.patch_all()

#standard library imports
import logging
import os
import json
import threading
from datetime import datetime

logger = logging.getLogger(__name__)

#third-party imports
import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from engineio.async_drivers import gevent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger

#local imports
from Backend.Scraper import (
    ErosScraper,
    EscortalligatorScraper,
    MegapersonalsScraper,
    RubratingsScraper,
    SkipthegamesScraper,
    YesbackpageScraper,
)
from Backend import database
from Backend.resultManager.appendResults import FolderAppender
from Backend.resultManager.resultManager import ResultManager


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

'''
    ---------------------------------
    Manage Scraper and threads
    ---------------------------------
'''


def list_threads():
    threads = threading.enumerate()
    if logger.isEnabledFor(logging.DEBUG):
        for thread in threads:
            logger.debug("Thread: %s (ID: %s)", thread.name, thread.ident)
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
            logger.info("Waiting for the scraper thread to finish...")
            self.scraper_thread.join()


    def manage_stop_scraper(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            self.scraper_thread.stop_thread()
            self.scraper_thread.join_with_timeout()  # Wait for the thread to finish
            logger.debug("Thread count after stop: %d", list_threads())
            return {"Response": "Scraper Thread Stopped Forcefully"}
        else:
            logger.debug("Thread count: %d (no active scraper)", list_threads())
            return {"Response": "No active Scraper Thread, Forceful Stop Attempted"}

    def get_scraper_status(self):
        logger.debug("Scraper status: %s", self.scraper_thread.is_alive() if self.scraper_thread else None)
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
        self._progress_callback = lambda phase, detail: socketio.emit(
            'scraper_update',
            {'status': 'running', 'phase': phase, 'detail': detail or ''}
        )
        self.scraper.set_progress_callback(self._progress_callback)

    def run(self):
        logger.debug("Thread count before scraper: %d", list_threads())
        while not self._stop_event.is_set() and not self.scraper.completed:
            socketio.emit('scraper_update', {'status': 'running', 'phase': 'starting', 'detail': ''})
            self.scraper.initialize()
        if self.scraper.completed:
            logger.info("Scraper completed")
            self.stop_thread()
        socketio.emit('scraper_update', {'status': 'completed'})

    def stop_thread(self):
        if not self.scraper.completed:
            self.scraper.stop_scraper()
        self._stop_event.set()

    def join_with_timeout(self, timeout=10):
        if not self.scraper.completed:
            self.join(timeout)
            if self.is_alive():
                logger.warning("ScraperThread did not terminate in time")

    def stopped(self):
        return self._stop_event.is_set()


# Defining Scraper Manager Obj for managing scraper and its thread
scraper_manager = ScraperManager()

'''
    ---------------------------------
    Result Manager functions
    ---------------------------------   
'''

# Initialized when user selects result directory; None until then (avoids NameError if handlers run first)
resultManager = None
folderAppend = None


def _require_result_manager():
    """Return True if resultManager and folderAppend are initialized, else emit error and return False."""
    global resultManager, folderAppend
    if resultManager is None or folderAppend is None:
        socketio.emit('result_folder_selected', {'error': 'Select a result directory first'})
        return False
    return True


def initialize_result_manager(result_dir):
    global resultManager
    resultManager = ResultManager(result_dir)

def initialize_folder_appender(result_dir):
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
    logger.info("Client connected")


# Scraper Manager Sockets
@socketio.on('scraper_status')
def get_status():
    scraper_manager.get_scraper_status()


@socketio.on('start_scraper')
def start_scraper(data):
    socketio.emit('scraper_update', {'status': 'started'})
    logger.debug("Start scraper request: %s", data)
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
    if not _require_result_manager():
        return
    logger.debug("Start append request: %s", data)
    socketio.emit('result_manager_update', {'status': 'appending'})
    folderAppend.setSelectedFolders(data)
    folderAppend.create_new_folder()
    folderAppend.append_files()
    folderAppend.save_data()
    response = 0
    return {'Response': response}


@socketio.on('open_PDF')
def open_PDF(data):
    if not _require_result_manager():
        return
    socketio.emit('result_manager_update', {'status': 'view_pdf'})
    response = resultManager.view_pdf(data)
    return {'Response': response}


@socketio.on('open_ss_dir')
def open_ss_dir(data):
    if not _require_result_manager():
        return
    socketio.emit('result_manager_update', {'status': 'view_SS_dir'})
    response = resultManager.view_ss_dir(data)
    return {'Response': response}


@socketio.on('open_clean_data')
def open_clean_data(data):
    if not _require_result_manager():
        return
    socketio.emit('result_manager_update', {'status': 'view_clean_data'})
    response = resultManager.view_clean_data(data)
    return {'Response': response}


@socketio.on('open_raw_data')
def open_raw_data(data):
    if not _require_result_manager():
        return
    socketio.emit('result_manager_update', {'status': 'view_raw_data'})
    response = resultManager.view_raw_data(data)
    return {'Response': response}


@socketio.on('open_diagram_dir')
def open_diagram_dir(data):
    if not _require_result_manager():
        return
    socketio.emit('result_manager_update', {'status': 'view_diagram_dir'})
    response = resultManager.view_diagram_dir(data)
    return {'Response': response}


def _get_qt_file_dialog():
    """Lazy-load Qt so the server can start without a display. Required only for directory picker."""
    from PyQt5.QtWidgets import QApplication, QFileDialog
    app_instance = QApplication.instance()
    if app_instance is None:
        app_instance = QApplication([])
    return QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())


def _initialize_from_result_dir(result_dir):
    """Initialize result manager and folder appender from a directory path."""
    initialize_result_manager(result_dir)
    initialize_folder_appender(result_dir)
    resultList = resultManager.get_folders()
    logger.info("Result directory selected: %s", result_dir)
    socketio.emit('result_folder_selected', {'folders': resultList, 'result_dir': result_dir})


@socketio.on('set_result_dir')
def set_result_dir():
    """Legacy: Opens Qt file dialog on server (may appear behind windows on Mac)."""
    directory = _get_qt_file_dialog()
    if not directory:
        return
    _initialize_from_result_dir(os.path.abspath(directory))


@socketio.on('set_result_dir_from_path')
def set_result_dir_from_path(data):
    """Uses path from Electron's native dialog (reliable on Mac)."""
    directory = data.get('path')
    if not directory or not os.path.isdir(directory):
        return
    _initialize_from_result_dir(os.path.abspath(directory))


@socketio.on('refresh_result_list')
def refresh_result_list():
    if not _require_result_manager():
        return
    resultManager.update_folders_json()
    resultList = resultManager.get_folders()
    # get_folders() returns (error_dict, 500) on failure; tuple is truthy so we must check explicitly
    if isinstance(resultList, tuple) and len(resultList) == 2 and resultList[1] == 500:
        socketio.emit('result_list_refreshed', {'error': resultList[0].get('error', 'Unknown error')})
    elif resultList:
        socketio.emit('result_list_refreshed', {'folders': resultList})
    else:
        socketio.emit('result_list_refreshed', {'error': 'No folders found in the selected directory'})

@socketio.on_error_default
def handle_error(e):
    logger.error("Socket error: %s", str(e))
    socketio.emit('scraper_update', {'status': 'error', 'error': str(e)})
    response = {"error": str(e)}
    return response, 500

@socketio.on('get_database_results')
def handle_database_results(data):
    logger.debug("get_database_results: %s", data)
    try:
        conn = database.connect(read_only=True)
    except psycopg.Error:
        socketio.emit('database_results', {'error': 'Could not connect to database'})
        return

    try:
        with conn.cursor(row_factory=dict_row) as cursor:
            table_name = data.get('tableName')
            cursor.execute(sql.SQL('SELECT * FROM {}').format(sql.Identifier(table_name)))
            results = cursor.fetchall()

            # Convert datetime objects to strings in the results
            serializable_results = []
            for row in results:
                if 'posted_on' in row and row['posted_on'] is not None:
                    row['posted_on'] = row['posted_on'].isoformat()
                if 'last_activity' in row and row['last_activity'] is not None:
                    row['last_activity'] = row['last_activity'].isoformat()
                if 'expires_on' in row and row['expires_on'] is not None:
                    row['expires_on'] = row['expires_on'].isoformat()
                serializable_results.append(row)

            socketio.emit('database_results', {'data': serializable_results})
    except Exception as e:
        logger.error("Database error: %s", str(e))
        socketio.emit('database_results', {'error': str(e)})
    finally:
        if conn:
            conn.close()


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
        logger.warning("File %s not found", file_path)
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from %s", file_path)

#------function called to save scraper updates after run------
def save_json(config, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(config, json_file, indent=4)

def process_scraper(scraper_name, scraper_settings):
        logger.info("Processing scraper: %s", scraper_name)
        start_scraper(scraper_settings['data'])
        scraper_manager.wait_for_scraper_to_complete()
        logger.info("Scraper %s processing complete", scraper_name)

def load_autoscraper_jobs():
        # Gets autoscrapers configurations from json file
        file_path = "server/scheduled_scrapers.json"
        config = load_json(file_path)
        
        # Gives any schedule scraper 2 hours to start from start time before terminating and not running
        scraper_grace_period = 7200  # time in seconds

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
                    logger.info("Scraper loaded: %s (ID: %s)", scraper_config_name, job_object.id)
                    config[scraper_config_name]["job_id"] = job_object.id
                    save_json(config, file_path)

                elif run_daily:
                    daily_cron_trigger = CronTrigger(hour=scraper_settings["hour"], minute=scraper_settings["minute"])
                    job_object = scheduler.add_job(run_scheduled_scraper, trigger=daily_cron_trigger, misfire_grace_time= scraper_grace_period, args=[scraper_config_name, "scrap"] )
                    logger.info("Scraper loaded: %s (ID: %s)", scraper_config_name, job_object.id)
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
            logger.info("Deleting scraper %s (finished all runs)", scraper_config_name)
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
                        logger.info("Deleting scraper %s (modified by user)", scraper_name)
                        scheduler.remove_job(job_id)
                # Rename/Deleted
                # Deleting from scheduler because the scraper in not in the json
                else:
                    logger.info("Deleting scraper %s (not in config)", scraper_name)
                    scheduler.remove_job(job_id)
        except Exception:
            logger.debug("Job is not a scraper")

#################Task Section for ApScheduler#########################
#------function called to manage_scrapers------
# manage scraper is called by our scheduler at the start up
# it will delete scrapers if they are modified, delete, or renamed
# it will also assign new scrapers or reassign modified scraper to the scheduler
def manage_scraper():
    delete_autoscraper_jobs()
    load_autoscraper_jobs()

#------function called to run scraper------
def run_scheduled_scraper(scraper_name, function_name):
    
    file_path = "server/scheduled_scrapers.json" 
    config = load_json(file_path)

    logger.debug("Checking scraper: %s, task: %s", scraper_name, function_name)
    if scraper_name in config:
        scraper_config = config[scraper_name]
        runs_left = scraper_config["runs_left"]

        # if a scraper was to run before getting deleted by the manager
        # The if statement would stop it
        if runs_left > 0:
            
            last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            scraper_config["last_run"] = last_run  # Updates last run time value
            scraper_config["runs_left"] -= 1  # Updates count of days/weeks left

            logger.info("Running scraper: %s (runs left: %d)", scraper_name, scraper_config['runs_left'])
            process_scraper(scraper_name, scraper_config)
            logger.info("Scraper finished: %s", scraper_name)
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
manage_schedule_trigger = CronTrigger(minute="*/15")

# Adds manage_scraper job to the scheduler
# Triggers every 15 minutes
# Uses default executor
# misfire_grace_time = lets thread exist for 15 minutes without firing
# if two manage_scraper job exist in queue, coalesce will make it fire only once for multiple instances
scheduler.add_job(manage_scraper, manage_schedule_trigger, executor="default", misfire_grace_time=900, coalesce=True)

# start scheduler
scheduler.start()



#-------------------------------Translator functions---------------------------------

#translate keywords function v0, current discussion topic is to move keywords/sets to a DB instead of a file.
#current state of this function is dormant, need to make changes to front end and determine keyword handling method for the future.

#2 - Function is called by socket.io translate and is passed language to translate the keywords file to
def translate_keywords(language):
    logger.info("Translating keywords to %s", language)
    with open('keywords.txt', 'r') as file:
        keywords = file.read().splitlines()

    translated_keywords = []
    for word in keywords:
        if word.strip():
            safe_word = str(word)
            translated_keywords.append(GoogleTranslator(source="auto", target=language).translate(safe_word)) 


#1 - When translate button is hit on front end, this function is called and data is passed to it
@socketio.on('translator')
def translator(language):
    logger.debug("translate_keywords(%s) called", language)
    translate_keywords(language)

#-------------------------------Translator End---------------------------------





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("Starting NetSpider server on http://127.0.0.1:5173 ...")
    print("(Ctrl+C to stop)")
    socketio.run(app, host='127.0.0.1', port=5173, allow_unsafe_werkzeug=True)
    
