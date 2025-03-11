from abc import ABC, abstractmethod
from typing import NamedTuple
import psycopg
from . import database


class ScraperPrototype(ABC):
    def __init__(self) -> None:
        self.location = None
        self.keywords: set[str] = set()
        self.join = None
        self.payment = None
        self.url = None
        self.text_search = None

    @abstractmethod
    def initialize(self):
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
    def check_for_payment_methods(self, description: str) -> bool:
        pass

    @abstractmethod
    def capture_screenshot(self, screenshot_name):
        pass

    @abstractmethod
    def check_and_append_keywords(self, data: str) -> None:
        pass

    @staticmethod
    def open_database() -> psycopg.Connection[NamedTuple]:
        """Open a connection to the database."""
        return database.connect()
