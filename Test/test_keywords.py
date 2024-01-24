import pytest
import os
import json
from Backend.Keywords import Keywords

class Test_Keywords:
    @pytest.fixture
    def keyword_object(self):
        key = Keywords()
        key.set_keywords_path('keywords.txt')
        key.set_keywords_sets_path('keywords_sets.json')
        return key

    def test_add_keywords(self, keyword_object):
        keyword_object.add_keywords('test1')
        with open('keywords.txt', 'r') as f:
            assert 'test1' in f.read()

    def test_remove_keywords(self, keyword_object):
        with open('keywords.txt', 'w') as f:
            f.write('test2\n')
            f.write('test3\n')

        keyword_object.remove_keywords('test2')
        with open('keywords.txt', 'r') as f:
            assert 'test2' not in f.read()

    def test_create_set(self, keyword_object):
        keyword_object.create_set('set1', ['test4', 'test5'])
        with open('keywords_sets.json', 'r') as f:
            sets = json.load(f)
            assert 'set1' in sets
            assert sets['set1'] == ['test4', 'test5']

    def test_remove_set(self, keyword_object):
        with open('keywords_sets.json', 'w') as f:
            json.dump({'set2': ['test6', 'test7']}, f)

        keyword_object.remove_set('set2')
        with open('keywords_sets.json', 'r') as f:
            sets = json.load(f)
            assert 'set2' not in sets

    def test_get_set_values(self, keyword_object):
        with open('keywords_sets.json', 'w') as f:
            json.dump({'set3': ['test8', 'test9']}, f)

        values = keyword_object.get_set_values('set3')
        assert values == ['test8', 'test9']

    def test_get_keywords(self, keyword_object):
        with open('keywords.txt', 'w') as f:
            f.write('test10\n')
            f.write('test11\n')

        keywords = keyword_object.get_keywords()
        assert keywords == ['test10', 'test11']

    def test_get_set(self, keyword_object):
        with open('keywords_sets.json', 'w') as f:
            json.dump({'set4': ['test12', 'test13']}, f)

        sets = keyword_object.get_set()
        assert sets == {'set4': ['test12', 'test13']}

    def test_remove_keyword_from_set(self, keyword_object):
        with open('keywords_sets.json', 'w') as f:
            json.dump({'set5': ['test14', 'test15']}, f)

        keyword_object.remove_keyword_from_set('test14', 'set5')
        with open('keywords_sets.json', 'r') as f:
            sets = json.load(f)
            assert sets['set5'] == ['test15']
