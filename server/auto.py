#Goal will be to have auto scraper looking for content in JSON file
#JSON file will determine when the scraper is run, what it runs, and how long it will run it. 


from app import ScraperManager
import json
import threading
import time


def start_and_stop_function():
    with open("scraper_schedule.json", 'r') as file:
        config = json.load(file)

    #loop through each item in JSON file. More logic to handle if 'daily' or 'weekly' is selected is needed
    for item in config:

        #get data from JSON file 
        frequency = item.get('frequency')
        duration = item.get('duration')
        data = item.get('data')

        stop_event = threading.Event()

        #start the scraper
        def run_function():
            while not stop_event.is_set():
                ScraperManager.start_scraper(data)
                time.sleep(frequency)

        #Create a thread to wait for time between start and stop scraping
        thread = threading.Thread(target=run_function)
        thread.start()

        #wait for scraping duration to finish, then call stop function to terminate the scraper thread
        time.sleep(duration)
        stop_event.set()
        ScraperManager.manage_stop_scraper()
        thread.join()

#plan is to have functionality that will not look at JSON file until first instance of setting up the auto scraper. 
# #After that, auto will run so long as backend is running. 
if __name__ == "__main__":
    start_and_stop_function()