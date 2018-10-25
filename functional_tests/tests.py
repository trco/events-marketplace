from django.test import LiveServerTestCase
from selenium import webdriver


class AddEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

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

        # he checks new url
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/events/add')

        # he sees page title and header
        self.assertIn('Events Marketplace', self.browser.title)
        header_text_two = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Event', header_text_two)

        # he fills out all the form fields

        # he submits the form

        # he is redirected to his dedicated profile page &
        # event is published at index

        # he sees all his published events
