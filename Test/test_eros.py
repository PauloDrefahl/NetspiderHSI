import pytest
from Backend.Scraper.ErosScraper import ErosScraper


class Test_ErosScraper:
    @pytest.fixture
    def scraper(self):
        scraper = ErosScraper()
        return scraper

    def test_get_cities(self, scraper):
        cities = scraper.get_cities()
        assert len(cities) == 5
        assert 'naples' in cities

    def test_set_city(self, scraper):
        scraper.set_city('naples')
        assert scraper.city == 'naples'

    def test_set_join_keywords(self, scraper):
        scraper.set_join_keywords()
        assert scraper.join_keywords == True

    def test_set_only_posts_with_payment_methods(self, scraper):
        scraper.set_only_posts_with_payment_methods()
        assert scraper.only_posts_with_payment_methods == True

    def test_get_formatted_url(self, scraper):
        scraper.set_city('naples')
        scraper.get_formatted_url()
        assert scraper.url == 'https://www.eros.com/florida/naples/sections/naples_escorts.htm'