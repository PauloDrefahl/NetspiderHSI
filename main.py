# import qdarkstyle as qdarkstyle
import psutil
from PyQt6.QtCore import Qt, QThread, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import time
import os
import subprocess
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtGui import QBrush, QColor
import GUI.Backend.Facade
import GUI.Backend.Keywords
from GUI.Ui_HSIWebScraper import Ui_HSIWebScraper
import chromedriver_autoinstaller_fix

# ---------------------------- Global Variable ----------------------------
# used to display popup message after scraping
popup_message = ''

# ---------------------------- Code to Show Icon on Windows Taskbar ----------------------------

basedir = os.path.dirname(__file__)
try:
    from ctypes import windll

    myappid = 'hsi.scraper.version1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

'''WARNING: To make changes to UI do NOT edit Ui_HSIWebScraper.py, instead make changes to UI using Qt Creator.
Then run the following command to convert the .ui file to .py:
pyuic6 Ui_HSIWebScraper.ui -o Ui_HSIWebScraper.py
OR
python -m PyQt6.uic.pyuic -o Ui_HSIWebScraper.py -x Ui_HSIWebScraper.ui

To make executable:
pyinstaller main.py --onefile --windowed --icon=ns.ico --name=NetSpider

'''


class MainBackgroundThread(QThread, QMainWindow):
    def __init__(self, ui, facade, website_selection, location, search_text, keywords_selected, inclusive_search,
                 include_payment_method, keywordlistWidget):
        QThread.__init__(self)
        self.ui = ui
        self.ui.keywordlistWidget = keywordlistWidget
        self.facade = facade
        self.website_selection = website_selection
        self.search_text = search_text
        self.include_payment_method = include_payment_method
        self.inclusive_search = inclusive_search
        self.keywords_selected = keywords_selected
        self.location = location

    def run(self):
        self.keywords_selected = set()

        # global variable used to display popup message after scraping
        global popup_message

        # find keywords selected in keyword list widget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).isSelected():
                self.keywords_selected.add(self.ui.keywordlistWidget.item(i).text())

        if self.search_text:
            self.keywords_selected.add(self.search_text)

        if self.website_selection == 'escortalligator':
            try:
                if self.inclusive_search:
                    self.facade.set_escortalligator_join_keywords()

                if self.include_payment_method:
                    self.facade.set_escortalligator_only_posts_with_payment_methods()

                self.facade.initialize_escortalligator_scraper(self.keywords_selected)
                popup_message = "success"
            except Exception as e:
                popup_message = str(e)
            time.sleep(2)

        if self.website_selection == 'megapersonals':
            try:
                if self.inclusive_search:
                    self.facade.set_megapersonals_join_keywords()

                if self.include_payment_method:
                    self.facade.set_megapersonal_only_posts_with_payment_methods()

                self.facade.initialize_megapersonals_scraper(self.keywords_selected)
                popup_message = "success"
            except Exception as e:
                popup_message = str(e)
            time.sleep(2)

        if self.website_selection == 'skipthegames':
            try:
                if self.inclusive_search:
                    self.facade.set_skipthegames_join_keywords()

                if self.include_payment_method:
                    self.facade.set_skipthegames_only_posts_with_payment_methods()

                self.facade.initialize_skipthegames_scraper(self.keywords_selected)
                popup_message = "success"
            except Exception as e:
                popup_message = str(e)
            time.sleep(2)

        if self.website_selection == 'yesbackpage':
            try:
                if self.inclusive_search:
                    self.facade.set_yesbackpage_join_keywords()

                if self.include_payment_method:
                    self.facade.set_yesbackpage_only_posts_with_payment_methods()

                self.facade.initialize_yesbackpage_scraper(self.keywords_selected)
                popup_message = "success"

            except Exception as e:
                popup_message = str(e)
            time.sleep(2)

        if self.website_selection == 'eros':
            try:
                if self.inclusive_search:
                    self.facade.set_eros_join_keywords()

                if self.include_payment_method:
                    self.facade.set_eros_only_posts_with_payment_methods()

                self.facade.initialize_eros_scraper(self.keywords_selected)
                popup_message = "success"
            except Exception as e:
                popup_message = str(e)
            time.sleep(2)

        # enable search button & settings tab
        self.ui.searchButton.setEnabled(True)
        self.ui.tabWidget.setTabEnabled(0, True)
        self.ui.keywordInclusivecheckBox.setChecked(False)
        self.ui.websiteSelectionDropdown.setEnabled(True)
        self.ui.setlocationDropdown.setEnabled(True)
        if self.website_selection == 'escortalligator' or self.website_selection == 'skipthegames':
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(False)
            self.ui.hideBrowserWhileRunningcheckBox.setChecked(False)
        else:
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)  # Create a QTimer instance
        self.timer.timeout.connect(self.update_timer)  # Connect the timeout signal to the update_timer method
        self.elapsed_time = 0  # Variable to store elapsed time
        self.worker = None
        self.worker_thread = None
        self.ui = Ui_HSIWebScraper()
        self.ui.setupUi(self)
        self.keywords_instance = GUI.Backend.Keywords()
        self.facade = GUI.Backend.Facade()

        self.central_widget = self.ui.tabWidget
        self.setCentralWidget(self.ui.tabWidget)

        # attributes used to handle events
        self.website_selection = ''
        self.include_payment_method = False
        self.inclusive_search = False
        self.search_mode = False
        self.search_text = ''
        self.keywords_selected = set()
        self.flagged_keywords = set()
        self.keys_to_add_to_new_set = []
        self.manual_keyword_selection = set()
        self.keywords_of_selected_set = set()
        self.set_keyword_selection = set()
        self.locations = []
        self.location = ''
        self.keywords = ''
        self.keyword_sets = ''



        # self.setStyleSheet(qdarkstyle.load_stylesheet('pyqt6'))

        # disable button until website is selected
        self.ui.searchButton_2.setEnabled(False)
        # bind websiteSelectionDropdown to website_selection_dropdown function
        self.ui.searchButton_2.clicked.connect(self.stop_button_clicked)

        ''' Bind GUI components to functions: '''
        # bind websiteSelectionDropdown to website_selection_dropdown function
        self.ui.websiteSelectionDropdown.currentIndexChanged.connect(self.website_selection_dropdown)

        # disable button until website is selected
        self.ui.searchButton.setEnabled(False)
        # bind searchButton to search_button_clicked function
        self.ui.searchButton.clicked.connect(self.search_button_clicked)

        # bind paymentMethodCheckBox to payment_method_check_box function
        self.ui.paymentMethodcheckBox.stateChanged.connect(self.payment_method_check_box)

        # bind selectAllKeywordscheckBox to select_all_keywords_check_box function
        self.ui.selectAllKeywordscheckBox.stateChanged.connect(self.select_all_keywords_check_box)

        # bind searchTextBox to search_text_box function
        self.ui.searchTextBox.textChanged.connect(self.search_text_box)

        # bind keywordlistWidget to keyword_list_widget function
        self.ui.keywordlistWidget.itemClicked.connect(self.keyword_list_widget)
        self.ui.keywordlistWidget.itemDoubleClicked.connect(self.flag_keywords)

        # bind keywordInclusivecheckBox to keyword_inclusive_chesck_box function
        self.ui.keywordInclusivecheckBox.stateChanged.connect(self.keyword_inclusive_check_box)
        self.ui.keywordInclusivecheckBox.setEnabled(False)

        self.ui.pushButton_2.clicked.connect(self.open_pdf_in_viewer)
        self.ui.pushButton_3.clicked.connect(self.open_pdf_in_viewer)
        self.ui.pushButton_4.clicked.connect(self.open_pdf_in_viewer)
        self.ui.pushButton_5.clicked.connect(self.open_pdf_in_viewer)

        # bind hideBrowserWhileRunningcheckBox to browser_mode function

        self.ui.hideBrowserWhileRunningcheckBox.stateChanged.connect(self.browser_mode)
        self.ui.hideBrowserWhileRunningcheckBox.setEnabled(False)

        # bind setSelectionDropdown to set_selection_dropdown function
        self.ui.setSelectionDropdown.currentIndexChanged.connect(self.set_selection_dropdown)

        # bind addKeywordButton to add_keyword_button_clicked function
        self.ui.addKeywordButton.clicked.connect(self.add_keyword_button_clicked)

        # bind removeKeywordButton to remove_keyword_button_clicked function
        self.ui.removeKeywordButton.clicked.connect(self.remove_keyword_button_clicked)

        # bind addSetButton to add_set_button_clicked function
        self.ui.addSetButton.clicked.connect(self.add_set_button_clicked)

        # bind removeSetButton to remove_set_button_clicked function
        self.ui.removeSetButton.clicked.connect(self.remove_set_button_clicked)

        # bind locationTextBox to location_text_box function
        self.ui.setlocationDropdown.currentIndexChanged.connect(self.set_location)

        # bind setFileSelectionButton to set_file_selection_button_clicked function
        self.keyword_sets_file_path = ''
        self.ui.setFileSelectionButton.clicked.connect(self.set_file_selection_button_clicked)

        # bind keywordfileSelectionButton to keyword_file_selection_button_clicked function
        self.keyword_file_path = ''
        self.ui.keywordfileSelectionButton.clicked.connect(self.keyword_file_selection_button_clicked)

        # bind storagePathSelectionButton to storage_path_selection_button_clicked function
        self.file_storage_path = ''
        self.ui.storagePathSelectionButton.clicked.connect(self.storage_path_selection_button_clicked)


        # self.keywords_instance.set_file_storage_path(self.file_storage_path)

        self.ui.pushButton.clicked.connect(self.login_button_clicked)

        self.ui.setList.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.tabWidget.setTabEnabled(3, False)

        self.ui.searchButton_3.clicked.connect(self.open_results_folder)

    ''' Functions used to handle events: '''

    def enable_tabs(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if username == "" and password == "":
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.tabWidget.setTabEnabled(3, True)
            self.ui.tabWidget.setCurrentIndex(1)

# file buttons
    def open_results_folder(self):
        os.startfile(os.path.realpath(self.file_storage_path))

    def storage_path_selection_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            save_path = file_dialog.selectedFiles()[0]

            QMessageBox.information(self, "Success", f"Selected path: {save_path}")
            self.file_storage_path = save_path
            self.enable_tabs()

            self.ui.storagePathOutput.setText(self.file_storage_path)
            self.ui.storagePathProgressBar.setValue(100)

            self.facade.set_storage_path(self.file_storage_path)
            self.ui.tabWidget.setCurrentIndex(2)

    def open_pdf_in_viewer(self):
        subprocess.Popen('NetSpider_quick_guide_v1.pdf', shell=True)

    def login_button_clicked(self):
        self.test_std_keyword_file()
        self.enable_tabs()

    def keyword_file_selection_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]

            if '.txt' in file_path:
                self.keyword_file_path = file_path
                self.enable_tabs()
                self.ui.keywordFilePathOutput.setText(self.keyword_file_path)
                self.ui.keywordFileProgressBar.setValue(100)

                self.keywords_instance.set_keywords_path(self.keyword_file_path)
                self.keywords = self.keywords_instance.get_keywords()
                self.initialize_keywords(self.keywords)
            else:
                QMessageBox.warning(self, "Error", "Please select 'keywords.txt'.")

    def test_std_keyword_file(self):
        file_path = "keywords.txt"

        self.keyword_file_path = file_path
        self.enable_tabs()
        self.ui.keywordFilePathOutput.setText(self.keyword_file_path)
        self.ui.keywordFileProgressBar.setValue(100)
        self.keywords_instance.set_keywords_path(self.keyword_file_path)
        self.keywords = self.keywords_instance.get_keywords()
        self.initialize_keywords(self.keywords)
        self.test_std_set_selection_button_clicked()

    def set_file_selection_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if 'keyword_sets.txt' in file_path:
                self.keyword_sets_file_path = file_path
                self.enable_tabs()

                self.ui.keywordSetsPathOutput.setText(self.keyword_sets_file_path)
                self.ui.keywordSetsProgressBar.setValue(100)

                self.keywords_instance.set_keywords_sets_path(self.keyword_sets_file_path)
                self.keyword_sets = self.keywords_instance.get_set()
                self.initialize_keyword_sets(self.keyword_sets)
            else:
                QMessageBox.warning(self, "Error", "Please select 'keyword_sets.txt'.")

    def test_std_set_selection_button_clicked(self):
        file_path = "keyword_sets.txt"

        self.keyword_sets_file_path = file_path
        self.enable_tabs()

        self.ui.keywordSetsPathOutput.setText(self.keyword_sets_file_path)
        self.ui.keywordSetsProgressBar.setValue(100)

        self.keywords_instance.set_keywords_sets_path(self.keyword_sets_file_path)
        self.keyword_sets = self.keywords_instance.get_set()
        self.initialize_keyword_sets(self.keyword_sets)
        self.test_std_set_file_path_button_clicked()

    def test_std_set_file_path_button_clicked(self):
        save_path = "result"
        self.file_storage_path = save_path
        self.enable_tabs()

        self.ui.storagePathOutput.setText(self.file_storage_path)
        self.ui.storagePathProgressBar.setValue(100)

        self.facade.set_storage_path(self.file_storage_path)

    # popup to confirm set removal

    def remove_set_popup_window(self, set_to_remove):
        popup = QtWidgets.QMessageBox.information(self, "Confirm Set Removal",
                                                  f"Are you sure you want to remove {set_to_remove} from the list of "
                                                  f"sets?", QtWidgets.QMessageBox.StandardButton.Yes |
                                                  QtWidgets.QMessageBox.StandardButton.No)

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    # remove set when button is clicked
    def remove_set_button_clicked(self):
        # get name of set to remove
        if self.ui.setList.currentItem() is not None:
            set_to_remove = self.ui.setList.currentItem().text()
        else:
            return

        confirmation = self.remove_set_popup_window(set_to_remove)
        if not confirmation:
            return

        # remove set from keyword_sets
        self.keywords_instance.remove_set(set_to_remove)

        # remove set from GUI
        self.ui.setList.takeItem(self.ui.setList.currentRow())

        # update list of sets
        self.ui.setSelectionDropdown.clear()
        self.ui.setSelectionDropdown.addItem('')
        self.keyword_sets = self.keywords_instance.get_set()
        self.ui.setSelectionDropdown.addItems(self.keyword_sets)

    # set location based on selection from the dropdown
    def set_location(self):
        self.location = self.ui.setlocationDropdown.currentText()

        if self.website_selection == 'eros':
            self.facade.set_eros_city(self.location)

        if self.website_selection == 'escortalligator':
            self.facade.set_escortalligator_city(self.location)

        if self.website_selection == 'yesbackpage':
            self.facade.set_yesbackpage_city(self.location)

        if self.website_selection == 'megapersonals':
            self.facade.set_megapersonals_city(self.location)

        if self.website_selection == 'skipthegames':
            self.facade.set_skipthegames_city(self.location)

    # initialize locations based on website that is selected
    def initialize_location_dropdown(self):
        self.ui.setlocationDropdown.clear()
        for location in self.locations:
            self.ui.setlocationDropdown.addItem(location)

    # add new set when button is clicked
    def add_set_button_clicked(self):
        # get name of new set
        sets = self.keywords_instance.get_set()

        if self.ui.newSetTextBox.text() != '':
            new_set_name = self.ui.newSetTextBox.text()
        else:
            return

        if self.ui.newSetTextBox.text() not in sets:
            # get text from list
            for item in self.ui.keywordList.selectedItems():
                self.keys_to_add_to_new_set.append(item.text())

            # call create_set function from keywords class
            self.keywords_instance.create_set(new_set_name, self.keys_to_add_to_new_set)

            # update list of sets
            self.ui.setList.addItem(new_set_name)

            # make self.keys_to_add_to_new_set of an empty list
            self.keys_to_add_to_new_set = []

            # add new set to setSelectionDropdown
            self.ui.setSelectionDropdown.addItem(new_set_name)

            # clear new set text box
            self.ui.newSetTextBox.clear()

        else:
            QMessageBox.warning(self, "Error", "Set name already exists.")

    # popup to confirm keyword removal
    def remove_keyword_popup_window(self, keyword_to_remove):
        popup = QtWidgets.QMessageBox.information(self, "Confirm Keyword Removal",
                                                  f"Are you sure you want to remove {keyword_to_remove} from the list "
                                                  f"of keywords? \n\nWarning: {keyword_to_remove} will be removed "
                                                  f"from all sets.", QtWidgets.QMessageBox.StandardButton.Yes |
                                                  QtWidgets.QMessageBox.StandardButton.No)

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    # remove new keyword
    def remove_keyword_button_clicked(self):
        # find text of selected item
        if self.ui.keywordList.currentItem() is not None:
            keyword = self.ui.keywordList.currentItem().text()
        else:
            return

        # confirm keyword removal
        confirmation = self.remove_keyword_popup_window(keyword)

        if not confirmation:
            return

        # keyword = keyword.encode('utf-8').decode('utf-8')
        self.remove_keyword(keyword)

        # loop through sets and remove keyword from each set
        for set_name in self.keyword_sets:
            if keyword in self.keywords_instance.get_set_values(set_name):
                self.keywords_instance.remove_keyword_from_set(keyword, set_name)

    # add new keyword
    def add_keyword_button_clicked(self):
        keyword = self.ui.newKeywordTextBox.text()

        if keyword != '':
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)
            # add keyword to text file
            self.keywords_instance.add_keywords(keyword)

            # clear new keyword text box
            self.ui.newKeywordTextBox.clear()

    # initialize all keywords to scraper tab
    def initialize_keywords(self, keywords):
        for keyword in keywords:
            self.ui.keywordlistWidget.addItem(keyword)
            self.ui.keywordList.addItem(keyword)

    # initialize all keyword sets to GUI
    def initialize_keyword_sets(self, keyword_sets):
        for keyword_set in keyword_sets:
            self.ui.setSelectionDropdown.addItem(keyword_set)
            self.ui.setList.addItem(keyword_set)

    # remove keyword from keywordlistWidget
    def remove_keyword(self, keyword):
        # remove keyword from keywordlistWidget using keyword text
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() == keyword:
                self.ui.keywordlistWidget.takeItem(i)
                self.ui.keywordList.takeItem(i)

                # remove from text file
                self.keywords_instance.remove_keywords(keyword)
                break

    # handle list of keywords to be searched
    def keyword_list_widget(self):
        for item in self.ui.keywordlistWidget.selectedItems():
            if item.text() not in self.keywords_of_selected_set and item.text() not in self.flagged_keywords:
                self.manual_keyword_selection.add(item.text())

        if (len(self.manual_keyword_selection) > 0 or len(self.keywords_selected) > 0) and self.website_selection != "":
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)
        if len(self.manual_keyword_selection) > 1:
            self.ui.keywordInclusivecheckBox.setEnabled(True)

        # if a keyword is unselected, remove it from the set
        for item in range(self.ui.keywordlistWidget.count()):
            keyword = self.ui.keywordlistWidget.item(item).text()
            if not self.ui.keywordlistWidget.item(item).isSelected():
                if keyword not in self.keywords_of_selected_set and keyword not in self.flagged_keywords:
                    self.manual_keyword_selection.discard(keyword)

        if not self.manual_keyword_selection and not self.search_text and not self.set_keyword_selection and not self.flagged_keywords:
            self.ui.keywordInclusivecheckBox.setEnabled(False)
        if self.website_selection != "" and (len(self.keywords_selected) > 0 or len(self.keywords_of_selected_set) > 0 or len(self.manual_keyword_selection) > 0):
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)

    def flag_keywords(self, item):
        keyword = item.text()

        # If the keyword is not already in the flagged keywords list, add it and highlight it
        if keyword not in self.flagged_keywords:
            self.flagged_keywords.add(keyword)
            self.keywords_selected.add(keyword)
            item.setSelected(True)
            item.setBackground(QBrush(QColor(255, 0, 0)))  # red background
        else:
            # If it's already flagged, remove it from the flagged keywords list and reset the background color
            self.flagged_keywords.remove(keyword)
            self.keywords_selected.remove(keyword)
            item.setSelected(False)
            item.setBackground(QBrush(QColor(255, 255, 255)))  # White background
        if self.website_selection != "" and (len(self.flagged_keywords) > 0 or len(self.keywords_selected) > 0 or len(self.keywords_of_selected_set) > 0):
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)

    # handle dropdown menu for keyword sets
    def set_selection_dropdown(self):
        selected_set = self.ui.setSelectionDropdown.currentText()

        if selected_set:
            self.ui.keywordInclusivecheckBox.setEnabled(True)
            self.set_keyword_selection = True

        # if empty set, unselect all keywords
        if selected_set == '':
            for i in range(self.ui.keywordlistWidget.count()):
                if self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                    self.ui.keywordlistWidget.item(i).setSelected(False)
                    self.keywords_of_selected_set = set()

            if not self.manual_keyword_selection and not self.search_text:
                self.ui.keywordInclusivecheckBox.setEnabled(False)
                self.set_keyword_selection = False
            if len(self.keywords_selected) == 0:
                self.ui.searchButton.setEnabled(False)
            if self.website_selection != "" and (
                    len(self.keywords_selected) > 0 or len(self.keywords_of_selected_set) > 0 or len(self.manual_keyword_selection) > 0):
                self.ui.searchButton.setEnabled(True)
            else:
                self.ui.searchButton.setEnabled(False)
            return

        # get keywords from selected set from keywords class
        self.keywords_of_selected_set = set(self.keywords_instance.get_set_values(selected_set))

        # select keywords_of_selected_set in keywordlistWidget
        for i in range(self.ui.keywordlistWidget.count()):
            if self.ui.keywordlistWidget.item(i).text() in self.keywords_of_selected_set:
                self.ui.keywordlistWidget.item(i).setSelected(True)

            elif self.ui.keywordlistWidget.item(i).text() not in self.manual_keyword_selection:
                self.ui.keywordlistWidget.item(i).setSelected(False)
        if self.website_selection != "" and (len(self.keywords_selected) > 0 or len(self.keywords_of_selected_set) > 0):
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)

    # scrape using text box input
    def search_text_box(self):
        self.search_text = self.ui.searchTextBox.text()
        if self.search_text != '':
            self.ui.keywordInclusivecheckBox.setEnabled(True)
        else:
            if not self.manual_keyword_selection and not self.set_keyword_selection:
                self.ui.keywordInclusivecheckBox.setEnabled(False)

    def keyword_inclusive_check_box(self):
        if self.ui.keywordInclusivecheckBox.isChecked():
            self.inclusive_search = True
        else:
            self.inclusive_search = False

    def browser_mode(self):
        if self.ui.hideBrowserWhileRunningcheckBox.isChecked():
            self.search_mode = True
        else:
            self.search_mode = False

    # if checked, select all items in list widget
    def select_all_keywords_check_box(self):
        if self.ui.selectAllKeywordscheckBox.isChecked():
            self.ui.selectAllKeywordscheckBox.setEnabled(True)
            # select all items in list widget
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(True)
                self.keywords_selected.add(
                    self.ui.keywordlistWidget.item(i).text())

            self.ui.keywordInclusivecheckBox.setEnabled(True)
        else:
            self.ui.setSelectionDropdown.setCurrentIndex(0)
            self.ui.selectAllKeywordscheckBox.setEnabled(False)
            self.keywords_selected = set()
            # deselect all items in list widget
            for i in range(self.ui.keywordlistWidget.count()):
                self.ui.keywordlistWidget.item(i).setSelected(False)
                if self.ui.keywordlistWidget.item(
                        i).text() in self.flagged_keywords:
                    self.flagged_keywords.remove(
                        self.ui.keywordlistWidget.item(i).text())
                    self.ui.keywordlistWidget.item(i).setBackground(
                        QBrush(QColor(255, 255, 255)))
            self.ui.keywordInclusivecheckBox.setEnabled(False)
        if self.website_selection != "" and len(self.keywords_selected) > 0:
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)

        # enable checkbox after it's unchecked
        self.ui.selectAllKeywordscheckBox.setEnabled(True)

    def payment_method_check_box(self):
        if self.ui.paymentMethodcheckBox.isChecked():
            self.ui.paymentMethodcheckBox.setEnabled(True)
            self.include_payment_method = True
        else:
            self.ui.paymentMethodcheckBox.setEnabled(False)
            self.include_payment_method = False

        # enable checkbox after it's unchecked
        self.ui.paymentMethodcheckBox.setEnabled(True)

    # handle dropdown menu for payment method
    def website_selection_dropdown(self):

        self.website_selection = self.ui.websiteSelectionDropdown.currentText()

        if self.website_selection != '' and (len(self.keywords_selected) > 0 or len(self.keywords_of_selected_set) > 0):
            self.ui.searchButton.setEnabled(True)
        else:
            self.ui.searchButton.setEnabled(False)
            self.ui.setlocationDropdown.clear()

        if self.website_selection == 'eros':
            self.locations = self.facade.get_eros_cities()
            self.set_location()
            self.initialize_location_dropdown()
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(True)

        if self.website_selection == 'escortalligator':
            self.locations = self.facade.get_escortalligator_cities()
            self.set_location()
            self.initialize_location_dropdown()
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(False)
            self.ui.hideBrowserWhileRunningcheckBox.setChecked(False)

        if self.website_selection == 'yesbackpage':
            self.locations = self.facade.get_yesbackpage_cities()
            self.set_location()
            self.initialize_location_dropdown()
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(True)

        if self.website_selection == 'megapersonals':
            self.locations = self.facade.get_megapersonals_cities()
            self.set_location()
            self.initialize_location_dropdown()
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(True)

        if self.website_selection == 'skipthegames':
            self.locations = self.facade.get_skipthegames_cities()
            self.set_location()
            self.initialize_location_dropdown()
            self.ui.hideBrowserWhileRunningcheckBox.setEnabled(False)
            self.ui.hideBrowserWhileRunningcheckBox.setChecked(False)

    def worker_finished(self):
        # success/fail message box
        global popup_message
        self.stop_timer()
        self.ui.keywordListLabel_4.setText("00:00:00")
        if popup_message == "success":
            self.ui.searchButton_2.setEnabled(False)
            QtWidgets.QMessageBox.information(self, "Success", "Success: Scraping completed successfully!")
        else:
            self.ui.searchButton_2.setEnabled(False)
            QtWidgets.QMessageBox.critical(self, "Error", "Error: Scraping not completed. Please try again.\n (Make "
                                                          "sure the latest version of Chrome is installed.)\n "
                                                          "Exact Error: "+ popup_message)

        popup_message = ''

    def search_button_clicked(self):
        self.elapsed_time = 0  # Reset elapsed time when the search button is pressed
        self.update_timer_label()  # Update the timer label with the initial value (0 seconds)
        self.timer.start(1000)
        start_time = time.time()  # Get the current time when the button is pressed
        self.ui.label_35.setPixmap(QtGui.QPixmap("GUI/photos/statusON.png"))
        self.ui.keywordListLabel_6.setText("ON")

        self.ui.searchButton.setEnabled(False)
        self.ui.tabWidget.setTabEnabled(0, False)
        self.ui.searchButton_2.setEnabled(True)
        self.ui.websiteSelectionDropdown.setEnabled(False)
        self.ui.setlocationDropdown.setEnabled(False)

        if self.website_selection == "yesbackpage":
            self.facade.yesbackpage_set_search_mode(self.search_mode)
            self.facade.set_yesbackpage_flagged_keywords(self.flagged_keywords)
        elif self.website_selection == "escortalligator":
            self.facade.escortalligator_set_search_mode(self.search_mode)
            self.facade.set_escortalligator_flagged_keywords(
                self.flagged_keywords)
        elif self.website_selection == "skipthegames":
            self.facade.skipthegames_set_search_mode(self.search_mode)
            self.facade.set_skipthegames_flagged_keywords(
                self.flagged_keywords)
        elif self.website_selection == "eros":
            self.facade.eros_set_search_mode(self.search_mode)
            self.facade.set_eros_flagged_keywords(self.flagged_keywords)
        elif self.website_selection == "megapersonals":
            self.facade.megapersonals_set_search_mode(self.search_mode)
            self.facade.set_megapersonals_flagged_keywords(
                self.flagged_keywords)

        # Set the search mode for the selected website (assuming you have the necessary code for this)

        self.worker = MainBackgroundThread(self.ui, self.facade, self.website_selection, self.location,
                                           self.search_text, self.keywords_selected, self.inclusive_search,
                                           self.include_payment_method, self.ui.keywordlistWidget)

        self.worker.finished.connect(self.worker_finished)
        self.worker.start()
        end_time = time.time()  # Get the current time when the scraping is completed
        elapsed_time = end_time - start_time  # Calculate the elapsed time

        print(f"Scraping started at: {start_time}")
        print(f"Scraping completed at: {end_time}")
        print(f"Elapsed time: {elapsed_time} seconds")

    def stop_button_clicked(self):
        self.ui.searchButton_2.setEnabled(False)
        if self.website_selection == 'yesbackpage':
            self.facade.stop_yesbackpage_scraper()
            self.worker_finished()

        elif self.website_selection == 'escortalligator':
            self.facade.stop_escortalligator_scraper()
            self.worker_finished()

        elif self.website_selection == 'skipthegames':
            self.facade.stop_skipthegames_scraper()
            self.worker_finished()

        elif self.website_selection == 'megapersonals':
            self.facade.stop_megapersonals_scraper()
            self.worker_finished()

        elif self.website_selection == 'eros':
            self.facade.stop_eros_scraper()
            self.worker_finished()
        self.worker.quit()
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'undetected_chromedriver.exe':
                try:
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass

    def update_timer(self):
        self.elapsed_time += 1  # Increment elapsed time by 1 second
        self.update_timer_label()  # Update the timer label with the new elapsed time

    def update_timer_label(self):
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60

        # Format the time as HH:MM:SS
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        # Update the timer label in your GUI with the current elapsed time (self.elapsed_time)
        # For example, if you have a QLabel called self.timerLabel:
        self.ui.keywordListLabel_4.setText(f"{formatted_time}")

    def stop_timer(self):
        self.timer.stop()  # Stop the timer manually (you can call this method when the user cancels the operation)
        self.ui.label_35.setPixmap(QtGui.QPixmap("GUI/photos/statusOFF2.png"))
        self.ui.keywordListLabel_6.setText("OFF")


# ---------------------------- GUI Main ----------------------------
if __name__ == "__main__":
    chromedriver_autoinstaller_fix.install()
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon(os.path.realpath("ns.ico")))
    window = MainWindow()
    window.show()
    app.exec()
