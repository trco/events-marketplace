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
        title_field = self.browser.find_element_by_id('id_title')
        title_field.send_keys('Test event #1')
        user_field = self.browser.find_element_by_id('id_user')
        user_field.send_keys('1')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')
        # he sees created event
        wait_for_row_in_table(self, 'Test event #1')

        # he visits Add Event page again
        self.browser.get(self.live_server_url + '/events/add')

        # he fills out & submits CreateEvent form once more
        title_field = self.browser.find_element_by_id('id_title')
        title_field.send_keys('Test event #2')
        user_field = self.browser.find_element_by_id('id_user')
        user_field.send_keys('1')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')
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
        self.event = Event.objects.create(
            title='Test event #1',
            user=self.user
        )

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
        self.assertRegex(redirect_url, f'/{ self.user.username }')
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
        self.assertRegex(redirect_url, f'/{ self.user.username }')
        # he sees updated event
        wait_for_row_in_table(self, 'Test event #2')

        # he checks that event is udpated at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        wait_for_row_in_table(self, 'Test event #2')


class UniqueProfilesOwnedEventsTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = User.objects.create_user(
            username='user_1',
            password='test1234'
        )
        self.user_2 = User.objects.create_user(
            username='user_2',
            password='test1234'
        )
        # create events
        self.event_1 = Event.objects.create(
            title='Test event #1',
            user=self.user_1
        )
        self.event_2 = Event.objects.create(
            title='Test event #2',
            user=self.user_2
        )

    def tearDown(self):
        self.browser.quit()

    # User story
    def test_users_have_unique_profile_with_owned_events(self):
        # user_1 visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user_1')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_login_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url_1 = self.browser.current_url
        self.assertRegex(redirect_url_1, f'/{ self.user_1.username }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test event #1', page_text)
        self.assertNotIn('Test event #2', page_text)

        # new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user_2 visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user_2')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_login_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url_2 = self.browser.current_url
        self.assertRegex(redirect_url_2, f'/{ self.user_2.username }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test event #2', page_text)
        self.assertNotIn('Test event #1', page_text)

        # check that first and second user's profile urls are different
        self.assertNotEqual(redirect_url_1, redirect_url_2)

    def test_user_has_readonly_access_to_other_user_profiles(self):
        # user_1 visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user_1')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_login_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url_1 = self.browser.current_url
        self.assertRegex(redirect_url_1, f'/{ self.user_1.username }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test event #1', page_text)
        self.assertIn('Edit', page_text)
        self.assertNotIn('Test event #2', page_text)

        # he visits user_2 profile
        self.browser.get(self.live_server_url + f'/{ self.user_2.username }')
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/{ self.user_2.username }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test event #2', page_text)
        self.assertNotIn('Test event #1', page_text)
        self.assertNotIn('Edit', page_text)
