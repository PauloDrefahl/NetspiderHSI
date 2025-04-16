#This file is designed to be run without the front or backend. 
#Goal is to test the scrapers quickly and efficiently. Just here for dev and testing.

#In the future, would be cool if could specify # pages to scrape before moving on?

from Backend.Scraper import (
    MegapersonalsScraper,
    SkipthegamesScraper,
    YesbackpageScraper,
    EscortalligatorScraper,
    ErosScraper,
    RubratingsScraper
)

#--------------------------------Test MegapersonalsScraper--------------------------------
def test_MegapersonalsScraper(headless_mode):

    scraper = MegapersonalsScraper()

    config = {'website': 'megapersonals', 
              'city': 'daytona', 
              'keywords': [], 
              'flagged_keywords': [], 
              'search_mode': headless_mode, 
              'search_text': '', 
              'payment_methods_only': False, 
              'inclusive_search': False, 
              'path': 'NetspiderHSI/result'
            }
    
    # Set path and city
    scraper.set_path(config['path'])
    scraper.set_city(config['city'])

    # Set flags
    scraper.set_search_mode(config['search_mode'])

    # Keywords
    scraper.set_keywords(set(config['keywords']))
    scraper.set_flagged_keywords(set(config['flagged_keywords']))

    if config['payment_methods_only']:
        scraper.set_only_posts_with_payment_methods()

    if config['inclusive_search']:
        scraper.set_join_keywords()

    # Run the scraper
    try:
        scraper.initialize()
        print("[✓] MegapersonalsScraper Scraper run complete.")
    except Exception as e:
        print(f"[✗] MegapersonalsScraper Scraper failed: {e}")


#--------------------------------Test SkipthegamesScraper--------------------------------
def test_SkipthegamesScraper(headless_mode):

    scraper = SkipthegamesScraper()

    config = {'website': 'skipthegames', 
              'city': 'bonita springs', 
              'keywords': [], 
              'flagged_keywords': [], 
              'search_mode': headless_mode, 
              'search_text': '', 
              'payment_methods_only': False, 
              'inclusive_search': False, 
              'path': 'NetspiderHSI/result'
            }
    
    # Set path and city
    scraper.set_path(config['path'])
    scraper.set_city(config['city'])

    # Set flags
    scraper.set_search_mode(config['search_mode'])

    # Keywords
    scraper.set_keywords(set(config['keywords']))
    scraper.set_flagged_keywords(set(config['flagged_keywords']))

    if config['payment_methods_only']:
        scraper.set_only_posts_with_payment_methods()

    if config['inclusive_search']:
        scraper.set_join_keywords()

    # Run the scraper
    try:
        scraper.initialize()
        print("[✓] SkipthegamesScraper Scraper run complete.")
    except Exception as e:
        print(f"[✗] SkipthegamesScraper Scraper failed: {e}")


#--------------------------------Test YesbackpageScraper--------------------------------
def test_YesbackpageScraper(headless_mode):

    scraper = YesbackpageScraper()

    config = {
        'website': 'yesbackpage', 
        'city': 'florida', 
        'keywords': [], 
        'flagged_keywords': [], 
        'search_mode': headless_mode, 
        'search_text': '', 
        'payment_methods_only': False, 
        'inclusive_search': False, 
        'path': 'NetspiderHSI/result'
    }
    
    # Set path and city
    scraper.set_path(config['path'])
    scraper.set_city(config['city'])

    # Set flags
    scraper.set_search_mode(config['search_mode'])

    # Keywords
    scraper.set_keywords(set(config['keywords']))
    scraper.set_flagged_keywords(set(config['flagged_keywords']))

    if config['payment_methods_only']:
        scraper.set_only_posts_with_payment_methods()

    if config['inclusive_search']:
        scraper.set_join_keywords()

    # Run the scraper
    try:
        scraper.initialize()
        print("[✓] YesbackpageScraper Scraper run complete.")
    except Exception as e:
        print(f"[✗] YesbackpageScraper Scraper failed: {e}")


#--------------------------------Test EscortalligatorScraper--------------------------------
def test_EscortalligatorScraper(headless_mode):

    scraper = EscortalligatorScraper()

    config = {
        'website': 'escortalligator',
        'city': 'orlando',
        'keywords': [],
        'flagged_keywords': [],
        'search_mode': headless_mode,
        'search_text': '',
        'payment_methods_only': False,
        'inclusive_search': False,
        'path': 'NetspiderHSI/result'
    }

    # Set path and city
    scraper.set_path(config['path'])
    scraper.set_city(config['city'])

    # Set flags
    scraper.set_search_mode(config['search_mode'])

    # Keywords
    scraper.set_keywords(set(config['keywords']))
    scraper.set_flagged_keywords(set(config['flagged_keywords']))

    if config['payment_methods_only']:
        scraper.set_only_posts_with_payment_methods()

    if config['inclusive_search']:
        scraper.set_join_keywords()

    # Run the scraper
    try:
        scraper.initialize()
        print("EscortalligatorScraper Scraper run complete.")
    except Exception as e:
        print(f"EscortalligatorScraper Scraper failed: {e}")


#--------------------------------Test ErosScraper--------------------------------
def test_ErosScraper(headless_mode):

    scraper = ErosScraper()

    config = {
        'website': 'eros', 
        'city': 'miami', 
        'keywords': [], 
        'flagged_keywords': [], 
        'search_mode': headless_mode, 
        'search_text': '', 
        'payment_methods_only': False, 
        'inclusive_search': False, 
        'path': 'NetspiderHSI/result'
    }

    # Set path and city
    scraper.set_path(config['path'])
    scraper.set_city(config['city'])

    # Set flags
    scraper.set_search_mode(config['search_mode'])

    # Keywords
    scraper.set_keywords(set(config['keywords']))
    scraper.set_flagged_keywords(set(config['flagged_keywords']))

    if config['payment_methods_only']:
        scraper.set_only_posts_with_payment_methods()

    if config['inclusive_search']:
        scraper.set_join_keywords()

    # Run the scraper
    try:
        scraper.initialize()
        print("ErosScraper Scraper run complete.")
    except Exception as e:
        print(f"ErosScraper Scraper failed: {e}")

#--------------------------------Test RubratingsScraper--------------------------------
def test_RubratingsScraper(headless_mode):

    scraper = RubratingsScraper()

    config = {
        'website': 'rubratings', 
        'city': 'fort myers', 
        'keywords': [], 
        'flagged_keywords': [], 
        'search_mode': headless_mode, 
        'search_text': '', 
        'payment_methods_only': False, 
        'inclusive_search': False, 
        'path': 'NetspiderHSI/result'
    }

    # Set path and city
    scraper.set_path(config['path'])
    scraper.set_city(config['city'])

    # Set flags
    scraper.set_search_mode(config['search_mode'])

    # Keywords
    scraper.set_keywords(set(config['keywords']))
    scraper.set_flagged_keywords(set(config['flagged_keywords']))

    if config['payment_methods_only']:
        scraper.set_only_posts_with_payment_methods()

    if config['inclusive_search']:
        scraper.set_join_keywords()

    # Run the scraper
    try:
        scraper.initialize()
        print("RubratingsScraper Scraper run complete.")
    except Exception as e:
        print(f"RubratingsScraper Scraper failed: {e}")




#--------------------------------Main function--------------------------------
if __name__ == "__main__":

    #Headless mode allows for scraping without displaying the browser window. 
    #set if you want no window (true) or window (false)
    headless_mode = True
    
    test_MegapersonalsScraper(headless_mode) 
    test_RubratingsScraper(headless_mode)
    test_EscortalligatorScraper(headless_mode)
    test_SkipthegamesScraper(headless_mode)
    test_YesbackpageScraper(headless_mode)
    test_ErosScraper(headless_mode)
