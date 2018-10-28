from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from events.models import Event
from .utils import wait_for_row_in_table


class AddEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )

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

        # he clicks Add Event link
        self.browser.find_element_by_link_text('Add Event').click()

        # he is redirected to login
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/accounts/login')

        # he fills out & submits login form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_login_btn').click()

        # he is redirected to the page with CreateEvent form
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/events/add')
        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text_two = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Event', header_text_two)

        # he fills out & submits CreateEvent form
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #1')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/profile/{ self.user.username }')
        # he sees created event
        wait_for_row_in_table(self, 'Test event #1')

        # he visits Add Event page again
        self.browser.get(self.live_server_url + '/events/add')

        # he fills out & submits CreateEvent form once more
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/profile/{ self.user.username }')
        # he sees both created events
        wait_for_row_in_table(self, 'Test event #1')
        wait_for_row_in_table(self, 'Test event #2')

        # he checks that both events are published at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        # he sees all his published events
        wait_for_row_in_table(self, 'Test event #1')
        wait_for_row_in_table(self, 'Test event #2')


class EditEventTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )
        # create event
        self.event = Event.objects.create(title='Test event #1')

    def tearDown(self):
        self.browser.quit()

    # User story
    def test_edit_event(self):
        # user visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_login_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/profile/{ self.user.username }')
        # he sees his events
        wait_for_row_in_table(self, 'Test event #1')

        # he clicks Edit button to edit event
        self.browser.find_element_by_id('id_edit_link').click()

        # he is redirected to the page with UpdateEvent form
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/edit/{ self.event.id }')

        # he updates event
        form_field = self.browser.find_element_by_id('id_title')
        form_field.send_keys('Test event #2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/profile/{ self.user.username }')
        # he sees updated event
        wait_for_row_in_table(self, 'Test event #2')

        # he checks that event is udpated at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        wait_for_row_in_table(self, 'Test event #2')
