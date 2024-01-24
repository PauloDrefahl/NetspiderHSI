import sys
import unittest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication, QListWidgetItem

from GUI.main import MainWindow

app = QApplication(sys.argv)
class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()

    def test_initialize_location_dropdown(self):
        self.window.locations = ['Location A', 'Location B', 'Location C']
        self.window.initialize_location_dropdown()
        expected_items = self.window.locations
        actual_items = [self.window.ui.setlocationDropdown.itemText(i) for i in
                        range(self.window.ui.setlocationDropdown.count())]
        self.assertEqual(actual_items, expected_items)

    def test_initialize_keywords(self):
        keywords = ['Keyword A', 'Keyword B', 'Keyword C']
        self.window.initialize_keywords(keywords)
        expected_items = keywords
        actual_items = [self.window.ui.keywordlistWidget.item(i).text() for i in
                        range(self.window.ui.keywordlistWidget.count())]
        self.assertEqual(actual_items, expected_items)
        actual_items = [self.window.ui.keywordList.item(i).text() for i in range(self.window.ui.keywordList.count())]
        self.assertEqual(actual_items, expected_items)

    def test_add_keyword_button_clicked(self):
        keyword_text = 'test keyword'
        self.window.keywords_instance = MagicMock()
        self.window.keywords_instance.add_keywords = MagicMock(return_value=None)
        self.window.ui.newKeywordTextBox.setText(keyword_text)
        self.window.add_keyword_button_clicked()
        expected_item = keyword_text
        actual_item = self.window.ui.keywordlistWidget.item(0).text()
        self.assertEqual(actual_item, expected_item)
        actual_item = self.window.ui.keywordList.item(0).text()
        self.assertEqual(actual_item, expected_item)
        self.window.keywords_instance.add_keywords.assert_called_once_with(keyword_text)
        expected_text = ''
        actual_text = self.window.ui.newKeywordTextBox.text()
        self.assertEqual(actual_text, expected_text)

    def test_remove_keyword(self):
        keyword_text = 'test keyword'
        keyword_item1 = QListWidgetItem(keyword_text)
        keyword_item2 = QListWidgetItem(keyword_text + '2')
        self.window.ui.keywordlistWidget.addItem(keyword_item1)
        self.window.ui.keywordlistWidget.addItem(keyword_item2)
        self.window.ui.keywordList.addItem(keyword_item1)
        self.window.ui.keywordList.addItem(keyword_item2)
        self.window.keywords_instance = MagicMock()
        self.window.keywords_instance.remove_keywords = MagicMock(return_value=None)
        self.window.remove_keyword(keyword_text)
        expected_count = 1
        actual_count = self.window.ui.keywordlistWidget.count()
        self.assertEqual(actual_count, expected_count)

    def test_keyword_list_widget(self):
        selected_item1 = QListWidgetItem('keyword 1')
        selected_item2 = QListWidgetItem('keyword 2')
        self.window.ui.keywordlistWidget.addItem(selected_item1)
        self.window.ui.keywordlistWidget.addItem(selected_item2)
        self.window.ui.keywordlistWidget.setCurrentItem(selected_item1)
        self.window.keywords_of_selected_set = {'keyword 2'}
        self.window.keyword_list_widget()
        expected_manual_selection = {'keyword 1'}
        actual_manual_selection = self.window.manual_keyword_selection
        self.assertEqual(actual_manual_selection, expected_manual_selection)
        selected_item3 = QListWidgetItem('keyword 3')
        self.window.ui.keywordlistWidget.addItem(selected_item3)
        self.window.ui.keywordlistWidget.setCurrentItem(selected_item3)
        self.window.keywords_of_selected_set = {'keyword 2'}

    def test_search_text_box(self):
        self.window.ui.searchTextBox.setText("Test search text")
        self.window.search_text_box()
        self.assertEqual(self.window.search_text, "Test search text")
        self.window.ui.searchTextBox.clear()
        self.window.search_text_box()
        self.assertEqual(self.window.search_text, "")


if __name__ == '__main__':
    unittest.main()
