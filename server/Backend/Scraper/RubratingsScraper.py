import os
import time
from datetime import datetime
import pandas as pd
from seleniumbase import Driver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Backend.ScraperPrototype import ScraperPrototype
import img2pdf
from openpyxl.styles import PatternFill


class RubratingsScraper(ScraperPrototype):

    def __init__(self):
        super().__init__()
        self.path = None
        self.driver = None
        self.cities = {
            "fort myers": 'http://rubsratings.com/list/index/39',
            "gainesville": 'http://rubsratings.com/list/index/40',
            "jacksonville": 'http://rubsratings.com/list/index/41',
            "miami": 'http://rubsratings.com/list/index/42',
            "ft lauderdale": 'http://rubsratings.com/list/index/43',
            "orlando": 'http://rubsratings.com/list/index/44',
            "panama city": 'http://rubsratings.com/list/index/45',
            "pensacola": 'http://rubsratings.com/list/index/46',
            "tallahassee": 'http://rubsratings.com/list/index/47',
            "tampa": 'http://rubsratings.com/list/index/48'
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
        # last_activity, phone_number, location, provider_id, post_title, description
        self.last_activity = []
        self.phone_number = []
        self.link = []
        self.location = []
        self.provider_id = []
        self.post_title = []
        self.description = []
        self.post_identifier = []
        self.payment_methods_found = []

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
        self.scraper_directory = f'{self.path}/rubratings-{self.city}-{self.date_time}'
        os.mkdir(self.scraper_directory)

        # Create directory for search screenshots
        self.screenshot_directory = f'{self.scraper_directory}/screenshots'
        self.pdf_filename = f'{self.screenshot_directory}/rubratings-{self.city}-{self.date_time}.pdf'
        os.mkdir(self.screenshot_directory)
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
        if self.search_mode:
            self.driver.get(self.url)
        else:
            self.driver.execute_script(f'window.open("{self.url}", "_blank");')
            original_window = self.driver.current_window_handle
            time.sleep(5)
            if len(self.driver.window_handles) >= 2:
                # Switch to the new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])

                # Close the original tab
                self.driver.switch_to.window(original_window)
                self.driver.close()

                # Switch back to the new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])

        # NOTE: Maximizing the window in headless mode makes it too big:
        # https://chromium.googlesource.com/chromium/src.git/+/f2bdeab65/ui/views/win/hwnd_message_handler_headless.cc#264
        if not self.search_mode:
            self.driver.maximize_window()
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[3]/button').click()
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    '''
    ---------------------------------------
    Getting the Data Running the Appending Functions and Getters
    ---------------------------------------
    '''
    def get_links(self) -> list:
        try:
            posts = self.driver.find_elements(By.CSS_SELECTOR, '.listing .list-img.lazy')  # Find specific elements
            links = []
            for post in posts:
                try:
                    parent_a = post.find_element(By.XPATH, './ancestor::a[1]')
                    link = parent_a.get_attribute('href')
                    links.append(link)
                except NoSuchElementException:
                    print("Parent <a> element not found for post element:", post)
        except NoSuchElementException:
            print("Posts elements not found")
            links = []
        return links

    def get_formatted_url(self) -> None:
        self.url = self.cities.get(self.city)

    def get_data(self, links) -> None:
        links = links

        counter = 0

        for link in links:
            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source
            #  looking for last_activity, phone_number, location, provider_id, post_title, description
            try:
                last_activity = self.driver.find_element(
                    By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/div/div/div[2]/div[3]/div[1]/ul/li[4]').text
            except NoSuchElementException:
                last_activity = 'N/A'
            try:
                phone_number_element = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div['
                                                                          '1]/div/div/div/div[2]/div[3]/div[1]/ul/li['
                                                                          '1]/a')
                phone_number = phone_number_element.get_attribute('data-replace')
                print("phone number: ", phone_number)
            except NoSuchElementException:
                phone_number = 'N/A'

            try:
                location = self.driver.find_element(
                    By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/div/div/div[2]/div[3]/div[1]/ul/li[2]'
                ).text

            except NoSuchElementException:
                location = 'N/A'
            try:
                provider_id_element = self.driver.find_element(
                    By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/div/div/div[2]/div[3]/div[1]/ul/li[3]'
                ).text
                provider_id = provider_id_element.split(':')[1].strip()  # Get everything after ':'

            except NoSuchElementException:
                provider_id = 'N/A'
            try:
                post_title = self.driver.find_element(
                    By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/div/div/div[2]/h3').text

            except NoSuchElementException:
                post_title = 'N/A'
            try:
                # Find the first element with the specified XPath
                first_element = self.driver.find_element(By.XPATH,
                                                         '/html/body/div[2]/div[3]/div/div[1]/div/div/div/div[2]/p[2] |'
                                                         '/html/body/div[2]/div[3]/div/div[1]/div/div/div/div[2]/h2[1]')

                # Determine if the first element is an <h2> element
                if first_element.tag_name == 'h2':
                    # If it's an <h2> element, find following sibling <h2> elements
                    following_elements = first_element.find_elements(By.XPATH, './following-sibling::h2')
                else:
                    # If it's a <p> element, find following sibling <p> elements
                    following_elements = first_element.find_elements(By.XPATH, './following-sibling::p')

                # Extract text from the first element
                description_texts = [first_element.text]

                # Extract text from all found elements
                description_texts.extend(element.text for element in following_elements)

                # Concatenate the descriptions into a single string
                description = ' '.join(description_texts)

                print("Concatenated Description:", description)
            except NoSuchElementException:
                print("Description elements not found")
                description = 'N/A'

            # reassign variables for each post
            self.number_of_keywords_in_post = 0
            self.keywords_found_in_post = []
            # last_activity, phone_number, location, provider_id, post_title, description
            if self.join_keywords and self.only_posts_with_payment_methods:
                if self.check_keywords(last_activity) or self.check_keywords(phone_number) or \
                        self.check_keywords(location) or self.check_keywords(provider_id) \
                        or self.check_keywords(post_title) or self.check_keywords(description):
                    self.check_keywords_found(last_activity, phone_number, location, provider_id, post_title,
                                              description, link)
                    counter = self.join_with_payment_methods(counter, link, last_activity, phone_number, location,
                                                             provider_id, post_title, description)

            elif self.join_keywords or self.only_posts_with_payment_methods:
                if self.join_keywords:
                    if self.check_keywords(last_activity) or self.check_keywords(phone_number) or \
                            self.check_keywords(location) or self.check_keywords(provider_id) \
                            or self.check_keywords(post_title) or self.check_keywords(description):
                        self.check_keywords_found(last_activity, phone_number, location, provider_id, post_title,
                                                  description, link)
                        counter = self.join_inclusive(counter, link, last_activity, phone_number, location, provider_id,
                                                      post_title, description)

                elif self.only_posts_with_payment_methods:
                    if len(self.keywords) > 0:
                        if self.check_keywords(last_activity) or self.check_keywords(phone_number) or \
                                self.check_keywords(location) or self.check_keywords(provider_id) \
                                or self.check_keywords(post_title) or self.check_keywords(description):
                            self.check_keywords_found(last_activity, phone_number, location, provider_id, post_title,
                                                      description, link)

                    counter = self.payment_methods_only(counter, link, last_activity, phone_number, location,
                                                        provider_id, post_title, description)
            else:
                # run if keywords
                if len(self.keywords) > 0:
                    if self.check_keywords(last_activity) or self.check_keywords(phone_number) or \
                            self.check_keywords(location) or self.check_keywords(provider_id) \
                            or self.check_keywords(post_title) or self.check_keywords(description):
                        self.check_keywords_found(last_activity, phone_number, location, provider_id, post_title,
                                                  description, link)
                        self.append_data(counter, link, last_activity, phone_number, location, provider_id,
                                         post_title, description)
                        screenshot_name = str(counter) + ".png"
                        self.capture_screenshot(screenshot_name)
                        counter += 1
                else:
                    self.append_data(counter, link, last_activity, phone_number, location, provider_id, post_title,
                                     description)
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
    def append_data(self, counter, link, last_activity, phone_number, location, provider_id, post_title, description):
        # last_activity, phone_number, location, provider_id, post_title, description
        self.post_identifier.append(counter)
        self.link.append(link)
        self.last_activity.append(last_activity)
        self.phone_number.append(phone_number)
        self.location.append(location)
        self.provider_id.append(provider_id)
        self.post_title.append(post_title)
        self.description.append(description)
        self.check_and_append_payment_methods(description)
        self.keywords_found.append(', '.join(self.keywords_found_in_post) or 'N/A')
        self.number_of_keywords_found.append(self.number_of_keywords_in_post or 'N/A')
        self.check_for_social_media(description)

    def join_inclusive(self, counter, link, last_activity, phone_number, location, provider_id, post_title,
                       description) -> int:
        if len(self.keywords) == len(set(self.keywords_found_in_post)):
            self.append_data(counter, link, last_activity, phone_number, location, provider_id, post_title,
                             description)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    def payment_methods_only(self, counter, link, last_activity, phone_number, location, provider_id, post_title,
                             description) -> int:

        if self.check_for_payment_methods(description):
            self.append_data(counter, link, last_activity, phone_number, location, provider_id, post_title,
                             description)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    def join_with_payment_methods(self, counter, link, last_activity, phone_number, location, provider_id,
                                  post_title, description) -> int:
        if self.check_for_payment_methods(description) and len(self.keywords) == len(set(self.keywords_found_in_post)):
            self.append_data(counter, link, last_activity, phone_number, location, provider_id, post_title, description)
            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)

            return counter + 1
        return counter

    # last_activity, phone_number, location, provider_id, post_title, description

    '''
    --------------------------
    Checking and Running Append
    --------------------------
    '''
    def check_keywords_found(self, last_activity, phone_number, location, provider_id, post_title, description, link) -> None:
        self.check_and_append_keywords(last_activity)
        self.check_and_append_keywords(phone_number)
        self.check_and_append_keywords(location)
        self.check_and_append_keywords(provider_id)
        self.check_and_append_keywords(post_title)
        self.check_and_append_keywords(description)
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
        # last_activity, phone_number, location, provider_id, post_title, description
        titled_columns = pd.DataFrame({
            'Post-identifier': self.post_identifier,
            'Link': self.link,
            # -------
            'Inputted City / Region': self.city,
            'Specified Location': self.location,
            'Last-Activity': self.last_activity,
            'Phone-Number': self.phone_number,
            'Provider-ID': self.provider_id,
            'Post-Title': self.post_title,
            'Description': self.description,
            # -------
            'Payment-methods': self.payment_methods_found,
            'Social-media-found': self.social_media_found,
            'Keywords-found': self.keywords_found,
            'Number-of-keywords-found': self.number_of_keywords_found
        })
        data = pd.DataFrame(titled_columns)
        with pd.ExcelWriter(
                f'{self.scraper_directory}/RAW-rubratings-{self.city}-{self.date_time}.xlsx',
                engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
            worksheet = writer.sheets['Sheet1']
            for i in range(2, worksheet.max_row):
                keywords = worksheet["L" + str(i)].value  # set the keywords var to each keyword in the cell
                for flagged_keyword in self.flagged_keywords:
                    if flagged_keyword in keywords:
                        worksheet["L" + str(i)].fill = PatternFill(
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
            f"{id_poster}"
            for id_poster in zip(
                self.provider_id
            )
        ]

        contact_info = [
            f"{phone_number}"
            for phone_number in zip(
                self.phone_number
            )
        ]

        overall_desc = [
            f"{post_title} ||| {description}"
            for post_title, description in zip(
                self.provider_id, self.description
            )
        ]

        post_time = [
            f"Last Activity: {last_active}"
            for last_active in zip(
                self.last_activity
            )
        ]

        titled_columns = pd.DataFrame({
            'Post-identifier': self.post_identifier,
            'Link': self.link,
            # ------
            'Inputted City / Region': self.city,
            'Specified Location': self.location,
            'Timeline': post_time,
            'Contacts': contact_info,
            'Personal Info': personal_info,
            'Overall Description': overall_desc,
            # ------
            'Payment-methods': self.payment_methods_found,
            'Social-media-found': self.social_media_found,
            'Keywords-found': self.keywords_found,
            'Number-of-keywords-found': self.number_of_keywords_found
        })
        data = pd.DataFrame(titled_columns)
        with pd.ExcelWriter(
                f'{self.scraper_directory}/CLEAN-rubratings-{self.city}-{self.date_time}.xlsx',
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

    def capture_screenshot(self, screenshot_name) -> None:
        try:
            # Wait for the picture under the 'pic' class to be visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.pic img'))
            )

            # Take screenshot after the picture is visible
            self.driver.save_screenshot(f'{self.screenshot_directory}/{screenshot_name}')
            self.create_pdf()
        except Exception as e:
            print(f"Error capturing screenshot: {e}")

    def create_pdf(self) -> None:
        screenshot_files = [os.path.join(self.screenshot_directory, filename) for filename in
                            os.listdir(self.screenshot_directory) if filename.endswith('.png')]
        with open(self.pdf_filename, "wb") as f:
            f.write(img2pdf.convert(screenshot_files))

    def reset_variables(self) -> None:
        # last_activity, phone_number, location, provider_id, post_title, description
        self.last_activity = []
        self.phone_number = []
        self.location = []
        self.provider_id = []
        self.post_title = []
        self.description = []
        self.link = []
        self.post_identifier = []
        self.payment_methods_found = []
        self.number_of_keywords_found = []
        self.only_posts_with_payment_methods = False
        self.join_keywords = False
        self.keywords_found = []
        self.social_media_found = []
