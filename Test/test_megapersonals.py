import pytest
from Backend.Scraper.MegapersonalsScraper import MegapersonalsScraper


class Test_Megapersonals:
    @pytest.fixture
    def scraper(self):
        scraper = MegapersonalsScraper()
        return scraper

    def test_get_cities(self, scraper):
        cities = scraper.get_cities()
        assert len(cities) == 20
        assert 'daytona' in cities

    def test_set_city(self, scraper):
        scraper.set_city('daytona')
        assert scraper.city == 'daytona'

    def test_set_join_keywords(self, scraper):
        scraper.set_join_keywords()
        assert scraper.join_keywords == True

    def test_set_only_posts_with_payment_methods(self, scraper):
        scraper.set_only_posts_with_payment_methods()
        assert scraper.only_posts_with_payment_methods == True

    def test_get_formatted_url(self, scraper):
        scraper.set_city('daytona')
        scraper.get_formatted_url()
        assert scraper.url == 'https://megapersonals.eu/public/post_list/109/1/1'
