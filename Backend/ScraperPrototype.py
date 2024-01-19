from abc import ABC, abstractmethod
from Backend.Keywords import Keywords


class ScraperPrototype(ABC):
    def __init__(self):
        self.location = None
        self.keywords = Keywords()
        self.join = None
        self.payment = None
        self.url = None
        self.text_search = None

    @abstractmethod
    def initialize(self, keywords):
        pass

    @abstractmethod
    def open_webpage(self):
        pass

    @abstractmethod
    def close_webpage(self):
        pass

    @abstractmethod
    def get_formatted_url(self):
        pass

    @abstractmethod
    def get_data(self, links):
        pass

    @abstractmethod
    def check_for_payment_methods(self, description):
        pass

    @abstractmethod
    def capture_screenshot(self, screenshot_name):
        pass

    @abstractmethod
    def check_keywords(self, text):
        pass

    @abstractmethod
    def check_and_append_keywords(self, text):
        pass
