from Backend.Scraper.EscortalligatorScraper import EscortalligatorScraper
from Backend.Scraper.MegapersonalsScraper import MegapersonalsScraper
from Backend.Scraper.SkipthegamesScraper import SkipthegamesScraper
from Backend.Scraper.YesbackpageScraper import YesbackpageScraper
from Backend.Scraper.ErosScraper import ErosScraper


class Facade:
    def __init__(self):
        self.eros = ErosScraper()
        self.escortalligator = EscortalligatorScraper()
        self.yesbackpage = YesbackpageScraper()
        self.megapersonals = MegapersonalsScraper()
        self.skipthegames = SkipthegamesScraper()

    def initialize_escortalligator_scraper(self, keywords):
        self.escortalligator.initialize(keywords)

    def stop_escortalligator_scraper(self):
        self.escortalligator.stop_scraper()

    def set_escortalligator_flagged_keywords(self, flagged_keywords):
        self.escortalligator.set_flagged_keywords(flagged_keywords)

    def set_escortalligator_city(self, city):
        self.escortalligator.set_city(city)

    def set_escortalligator_join_keywords(self):
        self.escortalligator.set_join_keywords()

    def get_escortalligator_cities(self):
        return self.escortalligator.get_cities()

    def escortalligator_set_search_mode(self, search_mode):
        self.escortalligator.set_search_mode(search_mode)

    def set_escortalligator_only_posts_with_payment_methods(self):
        self.escortalligator.set_only_posts_with_payment_methods()

    def initialize_megapersonals_scraper(self, keywords):
        self.megapersonals.initialize(keywords)

    def stop_megapersonals_scraper(self):
        self.megapersonals.stop_scraper()

    def set_megapersonals_flagged_keywords(self, flagged_keywords):
        self.megapersonals.set_flagged_keywords(flagged_keywords)

    def set_megapersonals_city(self, city):
        self.megapersonals.set_city(city)

    def set_megapersonals_join_keywords(self):
        self.megapersonals.set_join_keywords()

    def get_megapersonals_cities(self):
        return self.megapersonals.get_cities()

    def megapersonals_set_search_mode(self, search_mode):
        self.megapersonals.set_search_mode(search_mode)

    def set_megapersonal_only_posts_with_payment_methods(self):
        self.megapersonals.set_only_posts_with_payment_methods()

    def initialize_skipthegames_scraper(self, keywords):
        self.skipthegames.initialize(keywords)

    def set_skipthegames_flagged_keywords(self, flagged_keywords):
        self.skipthegames.set_flagged_keywords(flagged_keywords)

    def stop_skipthegames_scraper(self):
        self.skipthegames.stop_scraper()

    def set_skipthegames_city(self, city):
        self.skipthegames.set_city(city)

    def set_skipthegames_join_keywords(self):
        self.skipthegames.set_join_keywords()

    def get_skipthegames_cities(self):
        return self.skipthegames.get_cities()

    def skipthegames_set_search_mode(self, search_mode):
        self.skipthegames.set_search_mode(search_mode)

    def set_skipthegames_only_posts_with_payment_methods(self):
        self.skipthegames.set_only_posts_with_payment_methods()

    def initialize_yesbackpage_scraper(self, keywords):
        self.yesbackpage.initialize(keywords)

    def set_yesbackpage_flagged_keywords(self, flagged_keywords):
        self.yesbackpage.set_flagged_keywords(flagged_keywords)

    def set_yesbackpage_city(self, city):
        self.yesbackpage.set_city(city)

    def set_yesbackpage_join_keywords(self):
        self.yesbackpage.set_join_keywords()

    def get_yesbackpage_cities(self):
        return self.yesbackpage.get_cities()

    def stop_yesbackpage_scraper(self):
        self.yesbackpage.stop_scraper()

    def yesbackpage_set_search_mode(self, search_mode):
        self.yesbackpage.set_search_mode(search_mode)

    def set_yesbackpage_only_posts_with_payment_methods(self):
        self.yesbackpage.set_only_posts_with_payment_methods()

    def initialize_eros_scraper(self, keywords):
        self.eros.initialize(keywords)


    def set_eros_flagged_keywords(self, flagged_keywords):
        self.eros.set_flagged_keywords(flagged_keywords)

    def stop_eros_scraper(self):
        self.eros.stop_scraper()

    def set_eros_city(self, city):
        self.eros.set_city(city)

    def set_eros_join_keywords(self):
        self.eros.set_join_keywords()

    def get_eros_cities(self):
        return self.eros.get_cities()

    def eros_set_search_mode(self, search_mode):
        self.eros.set_search_mode(search_mode)

    def set_eros_only_posts_with_payment_methods(self):
        self.eros.set_only_posts_with_payment_methods()

    def set_storage_path(self, file_storage_path):
        if file_storage_path != '':
            self.yesbackpage.set_path(file_storage_path)
            self.skipthegames.set_path(file_storage_path)
            self.megapersonals.set_path(file_storage_path)
            self.escortalligator.set_path(file_storage_path)
            self.eros.set_path(file_storage_path)

