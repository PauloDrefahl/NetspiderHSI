import pytest
from Backend.Scraper.EscortalligatorScraper import EscortalligatorScraper

class Test_EscortalligatorScraper:
    @pytest.fixture
    def scraper(self):
        scraper = EscortalligatorScraper()
        return scraper

    def test_get_cities(self, scraper):
        cities = scraper.get_cities()
        assert len(cities) == 21
        assert 'orlando' in cities

    def test_set_city(self, scraper):
        scraper.set_city('orlando')
        assert scraper.city == 'orlando'

    def test_set_join_keywords(self, scraper):
        scraper.set_join_keywords()
        assert scraper.join_keywords == True

    def test_set_only_posts_with_payment_methods(self, scraper):
        scraper.set_only_posts_with_payment_methods()
        assert scraper.only_posts_with_payment_methods == True

    def test_get_formatted_url(self, scraper):
        scraper.set_city('orlando')
        scraper.get_formatted_url()
        assert scraper.url == 'https://escortalligator.com.listcrawler.eu/brief/escorts/usa/florida/orlando/1'