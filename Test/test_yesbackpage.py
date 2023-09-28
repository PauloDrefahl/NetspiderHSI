import pytest
from Backend.Scraper.YesbackpageScraper import YesbackpageScraper

class Test_YesbackpageScraper:
    @pytest.fixture
    def scraper(self):
        scraper = YesbackpageScraper()
        return scraper

    def test_get_cities(self, scraper):
        cities = scraper.get_cities()
        assert len(cities) == 21
        assert 'florida' in cities

    def test_set_city(self, scraper):
        scraper.set_city('florida')
        assert scraper.city == 'florida'

    def test_set_join_keywords(self, scraper):
        scraper.set_join_keywords()
        assert scraper.join_keywords == True

    def test_set_only_posts_with_payment_methods(self, scraper):
        scraper.set_only_posts_with_payment_methods()
        assert scraper.only_posts_with_payment_methods == True

    def test_get_formatted_url(self, scraper):
        scraper.set_city('florida')
        scraper.get_formatted_url()
        assert scraper.url == 'https://www.yesbackpage.com/-10/posts/8-Adult/'
