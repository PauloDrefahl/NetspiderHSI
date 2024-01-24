from Backend.Facade import Facade

class Test_Facade:
    def setup_method(self):
        self.facade = Facade()

    def test_set_escortalligator_city(self):
        city = 'fortmyers'
        self.facade.set_escortalligator_city(city)
        assert self.facade.escortalligator.city == city

    def test_set_escortalligator_join_keywords(self):
        self.facade.set_escortalligator_join_keywords()
        assert self.facade.escortalligator.join_keywords == True

    def test_get_escortalligator_cities(self):
        cities = self.facade.get_escortalligator_cities()
        assert isinstance(cities, list)

    def test_set_escortalligator_only_posts_with_payment_methods(self):
        self.facade.set_escortalligator_only_posts_with_payment_methods()
        assert self.facade.escortalligator.only_posts_with_payment_methods == True

    def test_set_megapersonals_city(self):
        city = 'naples'
        self.facade.set_megapersonals_city(city)
        assert self.facade.megapersonals.city == city

    def test_set_megapersonals_join_keywords(self):
        self.facade.set_megapersonals_join_keywords()
        assert self.facade.megapersonals.join_keywords == True

    def test_get_megapersonals_cities(self):
        cities = self.facade.get_megapersonals_cities()
        assert isinstance(cities, list)

    def test_set_megapersonal_only_posts_with_payment_methods(self):
        self.facade.set_megapersonal_only_posts_with_payment_methods()
        assert self.facade.megapersonals.only_posts_with_payment_methods == True

    def test_set_skipthegames_city(self):
        city = 'miami'
        self.facade.set_megapersonals_city(city)
        assert self.facade.megapersonals.city == city

    def test_set_skipthegames_join_keywords(self):
        self.facade.set_megapersonals_join_keywords()
        assert self.facade.megapersonals.join_keywords == True

    def test_get_skipthegames_cities(self):
        cities = self.facade.get_megapersonals_cities()
        assert isinstance(cities, list)

    def test_set_skipthegames_only_posts_with_payment_methods(self):
        self.facade.set_megapersonal_only_posts_with_payment_methods()
        assert self.facade.megapersonals.only_posts_with_payment_methods == True

    # eros
    def test_set_eros_city(self):
        city = 'orlando'
        self.facade.set_megapersonals_city(city)
        assert self.facade.megapersonals.city == city

    def test_set_eros_join_keywords(self):
        self.facade.set_megapersonals_join_keywords()
        assert self.facade.megapersonals.join_keywords == True

    def test_get_eros_cities(self):
        cities = self.facade.get_megapersonals_cities()
        assert isinstance(cities, list)

    def test_set_eros_only_posts_with_payment_methods(self):
        self.facade.set_megapersonal_only_posts_with_payment_methods()
        assert self.facade.megapersonals.only_posts_with_payment_methods == True

    # yesbackpage
    def test_set_yesbackpage_city(self):
        city = 'tampa'
        self.facade.set_megapersonals_city(city)
        assert self.facade.megapersonals.city == city

    def test_set_yesbackpage_join_keywords(self):
        self.facade.set_megapersonals_join_keywords()
        assert self.facade.megapersonals.join_keywords == True

    def test_get_yesbackpage_cities(self):
        cities = self.facade.get_megapersonals_cities()
        assert isinstance(cities, list)

    def test_set_yesbackpage_only_posts_with_payment_methods(self):
        self.facade.set_megapersonal_only_posts_with_payment_methods()
        assert self.facade.megapersonals.only_posts_with_payment_methods == True