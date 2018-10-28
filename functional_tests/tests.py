from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from events.models import Event
from .utils import wait_for_row_in_table


class AddEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # User story
    def test_visit_index_visit_add_event_create_event_visit_index(self):
        # user visits the index page
        self.browser.get(self.live_server_url)
        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Events Marketplace', header_text)

        # he clicks Add Event link & enters the page with CreateEvent form
        self.browser.find_element_by_link_text('Add Event').click()

        # he is redirected to the new url
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/events/add')
        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text_two = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Event', header_text_two)

        # he fills out all the form fields
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #1')
        # he submits the form & creates first event
        form_field.send_keys(Keys.ENTER)

        wait_for_row_in_table(self, 'Test event #1')

        # he creates second event
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #2')
        form_field.send_keys(Keys.ENTER)

        wait_for_row_in_table(self, 'Test event #1')
        wait_for_row_in_table(self, 'Test event #2')

        # TODO: he is redirected to his dedicated profile page with success msg

        # he checks that event is published at index
        self.browser.get(self.live_server_url)
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')
        # he sees all his published events
        wait_for_row_in_table(self, 'Test event #1')
        wait_for_row_in_table(self, 'Test event #2')


class EditEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        new_event = Event.objects.create(title='Test event #1')

    def tearDown(self):
        self.browser.quit()

    # User story
    def test_edit_event(self):
        # TODO: user logs in & visits his profile page

        # user visits Add Event page
        self.browser.get(self.live_server_url + '/events/add')
        wait_for_row_in_table(self, 'Test event #1')

        # he clicks Edit button & enters the page with UpdateEvent form
        self.browser.find_element_by_id('id_edit_link').click()

        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/events/edit/.+')

        # he changes event
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #2')
        form_field.send_keys(Keys.ENTER)

        wait_for_row_in_table(self, 'Test event #2')

        # TODO: he is redirected to his dedicated profile page with success msg

        # he checks that event is udpated at index
        self.browser.get(self.live_server_url)
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')
        wait_for_row_in_table(self, 'Test event #2')
