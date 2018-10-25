from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time


class AddEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # Helper functions
    MAX_WAIT = 10

    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        # infinite loop
        while True:
            try:
                table = self.browser.find_element_by_id('id_event_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                # return exception if more than 10s pass
                if time.time() - start_time > 10:
                    raise e
                # wait for 0.5s and retry
                time.sleep(0.5)

    # User story
    # user visits the index page
    def test_visit_index_visit_add_event_and_create_event(self):
        self.browser.get(self.live_server_url)

        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Events Marketplace', header_text)

        # he clicks Add Event link & enters the page with CreateEvent form
        self.browser.find_element_by_link_text('Add Event').click()

        # he is redirected to the new url
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/add')

        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text_two = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Event', header_text_two)

        # he fills out all the form fields
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #1')
        # he submits the form & creates first event
        form_field.send_keys(Keys.ENTER)

        self.wait_for_row_in_table('Test event #1')

        # he creates second event
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #2')

        form_field.send_keys(Keys.ENTER)

        self.wait_for_row_in_table('Test event #1')
        self.wait_for_row_in_table('Test event #2')

        # he is redirected to his dedicated profile page &
        # event is published at index

        # he sees all his published events
