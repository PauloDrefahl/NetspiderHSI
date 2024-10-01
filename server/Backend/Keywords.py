import json
import unicodedata


class Keywords:
    def __init__(self):
        self.keywords = []
        self.sets = {}
        self.keywords_path = ''
        self.keywords_set_path = ''

    def set_keywords_path(self, keyword_file_path):
        self.keywords_path = keyword_file_path

    def set_keywords_sets_path(self, keyword_sets_file_path):
        self.keywords_set_path = keyword_sets_file_path

    def add_keywords(self, keyword):
        # self.keywords.append(keyword)
        if self.keywords_path != '':
            with open(self.keywords_path, "r+", encoding='utf-8') as filename:
                content_set = filename.read().splitlines()
                if keyword not in content_set:
                    filename.write("\n" + keyword.lower())

    def remove_keywords(self, keyword):
        # self.keywords.remove(keyword)
        if self.keywords_path != '':
            with open(self.keywords_path, "r", encoding='utf-8') as filename:
                content_set = filename.read().splitlines()
                index = content_set.index(keyword.lower())

                content_set.remove(content_set[index])

            with open(self.keywords_path, "w", encoding='utf-8') as filename:
                filename.write("\n".join(content_set))

    def create_set(self, set_name, keywords_list):
        # self.sets[set_name.lower()] = keywords_list

        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r", encoding='utf-8') as readfile:
                read = readfile.read()
                if read != '':
                    self.sets = json.loads(read)
            self.sets[set_name.lower()] = keywords_list
            with open(self.keywords_set_path, "w", encoding='utf-8') as writefile:
                json.dump(self.sets, writefile)

    def remove_set(self, set_name):
        # del self.sets[set_name.lower()]

        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r", encoding='utf-8') as readfile:
                self.sets = json.loads(readfile.read())

            del self.sets[set_name.lower()]

            with open(self.keywords_set_path, 'w', encoding='utf-8') as writefile:
                json.dump(self.sets, writefile)

    def get_set_values(self, set_name):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r", encoding='utf-8') as readfile:
                self.sets = json.loads(readfile.read())

            return self.sets[set_name.lower()]

    def get_keywords(self):
        if self.keywords_path != '':
            with open(self.keywords_path, "r", encoding='utf-8') as filename:
                self.keywords = filename.read().splitlines()

            return self.keywords

    def get_set(self):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r", encoding='utf-8') as filename:
                self.sets = json.loads(filename.read())

            return self.sets

    def remove_keyword_from_set(self, keyword, set_name):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r", encoding='utf-8') as readfile:
                self.sets = json.loads(readfile.read())

            list_value = list(self.sets[set_name])
            list_value.remove(keyword)
            self.sets[set_name] = list_value

            with open(self.keywords_set_path, "w", encoding='utf-8') as writefile:
                json.dump(self.sets, writefile)

