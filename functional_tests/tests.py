from django.test import LiveServerTestCase
from selenium import webdriver


class AddEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # User story
    # user visits the index page
    def test_user_visits_index(self):
        self.browser.get(self.live_server_url)
        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Events Marketplace', header_text)
        # he clicks Add Event link & redirect to another url happens
        self.browser.find_element_by_link_text('Add Event').click()
        # he checks new url

    # he sees page title and header

    # he sees Add Event link

    # he click the link & enters the page with CreateEvent form

    # he fills out all the form fields

    # he submits the form

    # he is redirected to his dedicated profile page &
    # event is published at index

    # he sees all his published events
