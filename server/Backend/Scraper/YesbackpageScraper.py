import os
from datetime import datetime
import pandas as pd
from seleniumbase import Driver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Backend.ScraperPrototype import ScraperPrototype
import img2pdf
from openpyxl.styles import PatternFill
import threading


class YesbackpageScraper(ScraperPrototype):

    def __init__(self):
        super().__init__()
        self.path = None
        self.driver = None
        self.cities = {
            "florida": 'https://www.yesbackpage.com/-10/posts/8-Adult/',
            "broward": 'https://www.yesbackpage.com/70/posts/8-Adult/',
            "daytona beach": 'https://www.yesbackpage.com/71/posts/8-Adult/',
            "florida keys": 'https://www.yesbackpage.com/67/posts/8-Adult/',
            "ft myers-sw florida": 'https://www.yesbackpage.com/68/posts/8-Adult/',
            "gainesville": 'https://www.yesbackpage.com/72/posts/8-Adult/',
            "jacksonville": 'https://www.yesbackpage.com/73/posts/8-Adult/',
            "lakeland": 'https://www.yesbackpage.com/74/posts/8-Adult/',
            "miami": 'https://www.yesbackpage.com/75/posts/8-Adult/',
            "ocala": 'https://www.yesbackpage.com/76/posts/8-Adult/',
            "orlando": 'https://www.yesbackpage.com/77/posts/8-Adult/',
            "palm beach": 'https://www.yesbackpage.com/69/posts/8-Adult/',
            "panama city": 'https://www.yesbackpage.com/78/posts/8-Adult/',
            "pensacola-panhandle": 'https://www.yesbackpage.com/79/posts/8-Adult/',
            "sarasota-brandenton": 'https://www.yesbackpage.com/80/posts/8-Adult/',
            "space coast": 'https://www.yesbackpage.com/81/posts/8-Adult/',
            "st augustine": 'https://www.yesbackpage.com/82/posts/8-Adult/',
            "tallahassee": 'https://www.yesbackpage.com/83/posts/8-Adult/',
            "tampa bay area": 'https://www.yesbackpage.com/84/posts/8-Adult/',
            "treasure coast": 'https://www.yesbackpage.com/85/posts/8-Adult/',
            "west palm beach": 'https://www.yesbackpage.com/679/posts/8-Adult/'
        }
        self.city = ''
        self.url = ''
        self.known_payment_methods = ['cashapp', 'venmo', 'zelle', 'crypto', 'western union', 'no deposit',
                                      'deposit', ' cc ', 'card', 'credit card', 'applepay', 'donation', 'cash', 'visa',
                                      'paypal', ' mc ', 'mastercard']

        self.known_social_media = ['instagram', ' ig ', 'insta', 'snapchat', ' sc ', 'snap', 'onlyfans', 'only fans',
                                   'twitter', 'kik', 'skype', 'facebook', ' fb ', 'whatsapp', 'telegram',
                                   ' tg ', 'tiktok', 'tik tok']

        self.date_time = None
        self.scraper_directory = None
        self.screenshot_directory = None
        self.pdf_filename = None
        self.pdf = None
        self.keywords = set()
        self.flagged_keywords = set()
        self.search_mode = False
        self.completed = False

        self.join_keywords = False
        self.number_of_keywords_in_post = 0
        self.keywords_found_in_post = []

        self.only_posts_with_payment_methods = False

        # lists to store data and then send to csv file

        self.phone_number = []
        self.posted_on = []
        self.expires_on = []
        self.reply_to = []
        self.link = []
        self.name = []
        self.sex = []
        self.email = []
        self.location = []
        self.description = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.services = []

        self.number_of_keywords_found = []
        self.keywords_found = []
        self.social_media_found = []

    '''
    ---------------------------------------
    Set Data
    ---------------------------------------
    '''
    def get_cities(self) -> list:
        return list(self.cities.keys())

    def set_city(self, city) -> None:
        self.city = city

    def set_join_keywords(self) -> None:
        self.join_keywords = True

    def set_only_posts_with_payment_methods(self) -> None:
        self.only_posts_with_payment_methods = True

    def set_path(self, path) -> None:
        self.path = path

    def set_search_mode(self, search_mode) -> None:
        self.search_mode = search_mode

    def set_flagged_keywords(self, flagged_keywords) -> None:
        self.flagged_keywords = flagged_keywords

    def set_keywords(self, keywords) -> None:
        self.keywords = keywords

    '''
    ---------------------------------------
    Managing Scraper Run Time
    ---------------------------------------
    '''
    def initialize(self) -> None:
        # set keywords value
        # self.keywords = keywords
        # set up directories to save screenshots and Excel file.
        self.date_time = str(datetime.today())[0:19].replace(' ', '_').replace(':', '-')

        # Format website URL based on state and city
        self.get_formatted_url()
        self.driver = Driver(
            # Download the latest ChromeDriver for the current major version.
            driver_version="mlatest",
            undetectable=True,
            uc_subprocess=True,
            headless=self.search_mode,
            # Override the default mode (headless mode) on Linux.
            headed=not self.search_mode,
            # Use a fixed window size in headless mode.
            window_size="1920,1080" if self.search_mode else None,
        )

        # Open Webpage with URL
        self.open_webpage()

        # Find links of posts
        links = self.get_links()

        # Create directory for search data
        self.scraper_directory = f'{self.path}/yesbackpage-{self.city}-{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        self.pdf_filename = f'{self.screenshot_directory}/yesbackpage-{self.city}-{self.date_time}.pdf'
        os.mkdir(self.screenshot_directory)
        print("number of threads while running: ", threading.active_count())
        print("keywords inside scraper:", self.keywords)
        self.get_data(links)
        print("get data done")
        self.stop_scraper()
        print("closed webpage")
        self.reset_variables()
        print("reset variables")
        self.completed = True
        print("done scraping")

    def stop_scraper(self) -> None:
        self.driver.close()
        self.driver.quit()

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        # NOTE: Maximizing the window in headless mode makes it too big:
        # https://chromium.googlesource.com/chromium/src.git/+/f2bdeab65/ui/views/win/hwnd_message_handler_headless.cc#264
        if not self.search_mode:
            self.driver.maximize_window()
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    '''
    ---------------------------------------
    Getting the Data Running the Appending Functions and Getters
    ---------------------------------------
    '''
    def get_links(self) -> list:
        posts = self.driver.find_elements(
            By.CLASS_NAME, 'posttitle')
        links = [post.get_attribute('href') for post in posts]
        return links[2:]

    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)

    def get_data(self, links) -> None:
        links = links

        counter = 0

        for link in links:
            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/table[2]/tbody/'
                              'tr/td/div/p[2]').text
            except NoSuchElementException:
                description = 'N/A'

            try:
                timestamp = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/table[1]/tbody/'
                              'tr/td/div[3]/div[1]').text
                posted_on, expires_on, reply_to = self.parse_timestamp(timestamp)
            except NoSuchElementException:
                posted_on = 'N/A'
                expires_on = 'N/A'
                reply_to = 'N/A'

            # check if page contains "col-sm-6 offset-sm-3" which is the table that contains name, phone number, etc.
            if self.driver.find_elements(By.XPATH, '//*[@id="mainCellWrapper"]/div[1]/table/tbody/tr[1]/td/div[1]/div'):
                try:
                    name = self.driver.find_element(
                        By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                                  'tbody/tr[1]/td[2]').text[2:]
                except NoSuchElementException:
                    name = 'N/A'

                try:
                    sex = self.driver.find_element(
                        By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                                  'tbody/tr[2]/td[2]').text[2:]
                except NoSuchElementException:
                    sex = 'N/A'

                try:
                    phone_number = self.driver.find_element(
                        By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                                  'tbody/tr[6]/td[2]').text[2:]
                except NoSuchElementException:
                    phone_number = 'NA'

                try:
                    email = self.driver.find_element(
                        By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                                  'tbody/tr[8]/td[2]').text[2:]
                    # email = self.validate_email(email)
                except NoSuchElementException:
                    email = 'N/A'

                try:
                    location = self.driver.find_element(
                        By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td/div[1]/div/table/'
                                  'tbody/tr[9]/td[2]').text[2:]
                except NoSuchElementException:
                    location = 'N/A'

                try:
                    services = self.driver.find_element(
                        By.XPATH, '//*[@id="mainCellWrapper"]/div/table/tbody/tr/td/div[1]/div/table/'
                                  'tbody/tr[5]/td[2]').text[2:]
                except NoSuchElementException:
                    services = 'N/A'
            else:
                posted_on = 'N/A'
                expires_on = 'N/A'
                reply_to = 'N/A'
                name = 'N/A'
                sex = 'N/A'
                phone_number = 'N/A'
                email = 'N/A'
                location = 'N/A'
                services = 'N/A'

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []

            if self.join_keywords and self.only_posts_with_payment_methods:
                if self.check_keywords(description) or self.check_keywords(name) or self.check_keywords(sex) \
                        or self.check_keywords(phone_number) or self.check_keywords(email) \
                        or self.check_keywords(location) or self.check_keywords(services):
                    self.check_keywords_found(description, name, sex, phone_number, email, location, services, link)
                    counter = self.join_with_payment_methods(counter, description, email, link, location, name,
                                                             phone_number, services, sex, posted_on, expires_on, reply_to)

            elif self.join_keywords or self.only_posts_with_payment_methods:
                if self.join_keywords:
                    if self.check_keywords(description) or self.check_keywords(name) or self.check_keywords(sex) \
                            or self.check_keywords(phone_number) or self.check_keywords(email) \
                            or self.check_keywords(location) or self.check_keywords(services):
                        self.check_keywords_found(description, name, sex, phone_number, email, location, services, link)
                        counter = self.join_inclusive(counter, description, email, link, location, name, phone_number,
                                                      services, sex, posted_on, expires_on, reply_to)

                elif self.only_posts_with_payment_methods:
                    if len(self.keywords) > 0:
                        if self.check_keywords(description) or self.check_keywords(name) or self.check_keywords(sex) \
                                or self.check_keywords(phone_number) or self.check_keywords(email) \
                                or self.check_keywords(location) or self.check_keywords(services):
                            self.check_keywords_found(description, name, sex, phone_number, email, location, services, link)

                    counter = self.payment_methods_only(counter, description, email, link, location, name,
                                                        phone_number, services, sex, posted_on, expires_on, reply_to)
            else:
                # run if keywords
                if len(self.keywords) > 0:
                    if self.check_keywords(description) or self.check_keywords(name) or self.check_keywords(sex) \
                            or self.check_keywords(phone_number) or self.check_keywords(email) \
                            or self.check_keywords(location) or self.check_keywords(services):
                        self.check_keywords_found(description, name, sex, phone_number, email, location, services, link)
                        self.append_data(counter, description, email, link, location, name, phone_number, services,
                                         sex, posted_on, expires_on, reply_to)
                        screenshot_name = str(counter) + ".png"
                        self.capture_screenshot(screenshot_name)
                        counter += 1
                else:
                    self.append_data(counter, description, email, link, location, name, phone_number, services,
                                     sex, posted_on, expires_on, reply_to)
                    screenshot_name = str(counter) + ".png"
                    self.capture_screenshot(screenshot_name)
                    counter += 1
            self.RAW_format_data_to_excel()
            self.CLEAN_format_data_to_excel()

    '''
    --------------------------
    Appending Data
    --------------------------
    '''
    def append_data(self, counter, description, email, link, location, name, phone_number, services, sex, posted_on, expires_on, reply_to):
        self.post_identifier.append(counter)
        self.posted_on.append(posted_on)
        self.expires_on.append(expires_on)
        self.reply_to.append(reply_to)
        self.link.append(link)
        self.description.append(description)
        self.name.append(name)
        self.sex.append(sex)
        self.phone_number.append(phone_number)
        self.email.append(email)
        self.location.append(location)
        self.check_and_append_payment_methods(description)
        self.services.append(services)
        self.keywords_found.append(', '.join(self.keywords_found_in_post) or 'N/A')
        self.number_of_keywords_found.append(self.number_of_keywords_in_post or 'N/A')
        self.check_for_social_media(description)

    def join_with_payment_methods(self, counter, description, email, link, location, name, phone_number,
                                  services, sex, posted_on, expires_on, reply_to) -> int:
        if self.check_for_payment_methods(description) and len(self.keywords) == len(set(self.keywords_found_in_post)):
            self.append_data(counter, description, email, link, location, name, phone_number, services,
                             sex, posted_on, expires_on, reply_to)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    def join_inclusive(self, counter, description, email, link, location, name, phone_number, services, sex, posted_on, expires_on, reply_to) -> int:
        if len(self.keywords) == len(set(self.keywords_found_in_post)):
            self.append_data(counter, description, email, link, location, name, phone_number, services,
                             sex, posted_on, expires_on, reply_to)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    def payment_methods_only(self, counter, description, email, link, location, name, phone_number,
                             services, sex, posted_on, expires_on, reply_to) -> int:

        if self.check_for_payment_methods(description):
            self.append_data(counter, description, email, link, location, name, phone_number, services,
                             sex, posted_on, expires_on, reply_to)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    '''
    --------------------------
    Checking and Running Append
    --------------------------
    '''
    def check_keywords_found(self, description, name, sex, phone_number, email, location, services, link) -> None:
        self.check_and_append_keywords(description)
        self.check_and_append_keywords(name)
        self.check_and_append_keywords(sex)
        self.check_and_append_keywords(phone_number)
        self.check_and_append_keywords(email)
        self.check_and_append_keywords(location)
        self.check_and_append_keywords(services)
        self.check_and_append_keywords(link)

    def check_for_payment_methods(self, description) -> bool:
        for payment in self.known_payment_methods:
            if payment in description.lower():
                return True
        return False

    def check_and_append_payment_methods(self, description) -> None:
        payments = ''
        for payment in self.known_payment_methods:
            if payment in description.lower():
                payments += payment + '\n'

        if payments != '':
            self.payment_methods_found.append(payments)
        else:
            self.payment_methods_found.append('N/A')

    def check_for_social_media(self, description) -> None:
        social_media = ''
        for social in self.known_social_media:
            if social in description.lower():
                social_media += social + '\n'

        if social_media != '':
            self.social_media_found.append(social_media)
        else:
            self.social_media_found.append('N/A')

    def check_keywords(self, data) -> bool:
        for key in self.keywords:
            if key in data.lower():
                return True
        return False

    def check_and_append_keywords(self, data) -> None:
        for key in self.keywords:
            if key in data.lower():
                self.keywords_found_in_post.append(key)
                self.number_of_keywords_in_post += 1

    '''
    ---------------------------------
    Formatting Data and Result Creation
    ---------------------------------
    '''
    def RAW_format_data_to_excel(self) -> None:
        titled_columns = pd.DataFrame({
            'Post-identifier': self.post_identifier,
            'Link': self.link,
            # -------
            'Inputted City / Region': self.city,
            'Specified Location': self.location,
            'Posted On': self.posted_on,
            'Expires On': self.expires_on,
            'Phone-Number': self.phone_number,
            'E-mail': self.email,
            'Name': self.name,
            'Sex': self.sex,
            'Reply To': self.reply_to,
            'Description': self.description,
            'Services': self.services,
            # -------
            'Payment-methods': self.payment_methods_found,
            'Social-media-found': self.social_media_found,
            'Keywords-found': self.keywords_found,
            'Number-of-keywords-found': self.number_of_keywords_found
        })
        data = pd.DataFrame(titled_columns)
        with pd.ExcelWriter(
                f'{self.scraper_directory}/RAW-yesbackpage-{self.city}-{self.date_time}.xlsx',
                engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
            worksheet = writer.sheets['Sheet1']
            for i in range(2, worksheet.max_row):
                keywords = worksheet["N" + str(i)].value  # set the keywords var to each keyword in the cell
                for flagged_keyword in self.flagged_keywords:
                    if flagged_keyword in keywords:
                        worksheet["N" + str(i)].fill = PatternFill(
                            fill_type='solid',
                            start_color='ff0000',
                            end_color='ff0000')
                        worksheet["A" + str(i)].fill = PatternFill(
                            fill_type='solid',
                            start_color='ff0000',
                            end_color='ff0000')

            for col in worksheet.columns:  # dynamically adjust column sizes based on content of cell
                max_length = 0
                col = [cell for cell in col]
                for cell in col:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[
                    col[0].column_letter].width = adjusted_width

    def CLEAN_format_data_to_excel(self) -> None:
        personal_info = [
            f"{name} ||| {sex} "
            for name, sex in zip(
                self.name, self.sex
            )
        ]

        contact_info = [
            f"{phone_number} ||| {email}"
            for phone_number, email in zip(
                self.phone_number, self.email
            )
        ]

        overall_desc = [
            f"{description} ||| {services} ||| {Reply_to}"
            for description, services, Reply_to in zip(
                self.description, self.services, self.reply_to
            )
        ]

        post_time = [
            f" Posted on: {posted_on} Expires on: {expires_on}"
            for posted_on, expires_on in zip(
                self.posted_on, self.expires_on
            )
        ]

        titled_columns = pd.DataFrame({
            'Post-identifier': self.post_identifier,
            'Link': self.link,
            # ------
            'Inputted City / Region': self.city,
            'Specified Location': self.location,
            'Timeline': self.posted_on,
            'Contacts': contact_info,
            'Personal Info': personal_info,
            'Overall Description': overall_desc,
            # -----
            'Payment-methods': self.payment_methods_found,
            'Social-media-found': self.social_media_found,
            'Keywords-found': self.keywords_found,
            'Number-of-keywords-found': self.number_of_keywords_found
        })
        data = pd.DataFrame(titled_columns)
        with pd.ExcelWriter(
                f'{self.scraper_directory}/CLEAN-yesbackpage-{self.city}-{self.date_time}.xlsx',
                engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
            worksheet = writer.sheets['Sheet1']
            for i in range(2, worksheet.max_row):
                keywords = worksheet["K" + str(i)].value  # set the keywords var to each keyword in the cell
                for flagged_keyword in self.flagged_keywords:
                    if flagged_keyword in keywords:
                        worksheet["K" + str(i)].fill = PatternFill(
                            fill_type='solid',
                            start_color='ff0000',
                            end_color='ff0000')
                        worksheet["A" + str(i)].fill = PatternFill(
                            fill_type='solid',
                            start_color='ff0000',
                            end_color='ff0000')

            for col in worksheet.columns:  # dynamically adjust column sizes based on content of cell
                max_length = 0
                col = [cell for cell in col]
                for cell in col:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[
                    col[0].column_letter].width = adjusted_width

    def parse_timestamp(self, timestamp_str):
        # Initialize all parts as 'N/A' to handle missing parts
        posted_on, updated_on, expires_on, reply_to = ('N/A',) * 4

        # Split the string by 'Expires On:' to separate the first half and the 'Expires On:' part
        parts = timestamp_str.split('Expires On:')
        first_half = parts[0].strip() if len(parts) > 0 else 'N/A'

        # Check if 'Updated On:' is in the first half
        if 'Updated On:' in first_half:
            posted_on, updated_on = first_half.split('Updated On:')
            posted_on = posted_on.replace('Posted on:', '').strip()
            updated_on = updated_on.strip()
        else:
            # If there's no 'Updated On:', the whole first half is 'Posted on:'
            posted_on = first_half.replace('Posted on:', '').strip()

        # Now, handle the 'Expires On:' part
        if len(parts) > 1:
            second_half = parts[1].strip()
            if 'Reply to:' in second_half:
                expires_on, reply_to = second_half.split('Reply to:')
                expires_on = expires_on.strip()
                reply_to = reply_to.strip()
            else:
                expires_on = second_half.strip()

        print(f"Posted on: {posted_on}")
        print(f"Updated on: {updated_on if updated_on != 'N/A' else 'No update info'}")
        print(f"Expires on: {expires_on}")
        print(f"Reply to: {reply_to if reply_to != 'N/A' else 'No reply info'}")

        return posted_on, expires_on, reply_to

    def validate_email(self, email):
        return email if "@" in email else "N/A"

    def capture_screenshot(self, screenshot_name) -> None:
        self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')
        self.create_pdf()

    def create_pdf(self) -> None:
        screenshot_files = [os.path.join(self.screenshot_directory, filename) for filename in os.listdir(self.screenshot_directory) if filename.endswith('.png')]
        with open(self.pdf_filename, "wb") as f:
            f.write(img2pdf.convert(screenshot_files))

    def reset_variables(self) -> None:
        self.phone_number = []
        self.posted_on = []
        self.expires_on = []
        self.reply_to = []
        self.link = []
        self.name = []
        self.sex = []
        self.email = []
        self.location = []
        self.description = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.services = []
        self.number_of_keywords_found = []
        self.only_posts_with_payment_methods = False
        self.join_keywords = False
        self.keywords_found = []
        self.social_media_found = []
