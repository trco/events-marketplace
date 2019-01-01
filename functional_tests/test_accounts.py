from selenium import webdriver
from .base import FunctionalTest


class SignUpTest(FunctionalTest):

    def test_visitor_can_signup_and_login(self):
        # user visits signup page
        self.browser.get(self.live_server_url + '/accounts/signup/')

        # user fills out & submits signup form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_signup_btn').click()

        # user is redirected to the login page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/accounts/login')

        # user can login with newly created credentials
        self.login_user('user', 'test1234')

        # user is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/user')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('User profile', header_text)


class AccessToUserProfilesTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Event 1', self.user_1)
        self.event_2 = self.create_event('Event 2', self.user_2)

    def test_readonly_and_write_access_to_profiles(self):
        # user_1 visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # user_1 fills out & submits login form
        self.login_user('user_1', 'test1234')

        # user_1 is redirected to his dedicated profile page
        redirect_url_1 = self.browser.current_url
        self.assertRegex(redirect_url_1, f'/{ self.user_1.username }')

        # user_1 has write access to his events
        self.wait_for_text_in_body('Event 1', 'Edit')
        self.wait_for_text_in_body('Event 2', not_in=True)

        # new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user_2 visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # user_2 fills out & submits login form
        self.login_user('user_2', 'test1234')

        # user_2 is redirected to his dedicated profile page
        redirect_url_2 = self.browser.current_url
        self.assertRegex(redirect_url_2, f'/{ self.user_2.username }')

        # user_2 has write access to his events
        self.wait_for_text_in_body('Event 2', 'Edit')
        self.wait_for_text_in_body('Event 1', not_in=True)

        # check that redirect urls are different for each user
        self.assertNotEqual(redirect_url_1, redirect_url_2)

        # user_2 visits user_1 profile
        self.browser.get(self.live_server_url + f'/{ self.user_1.username }')
        self.wait_for_text_in_body('Event 1')

        # user_1 has readonly access to user_1 profile
        self.wait_for_text_in_body('Edit', 'Event 2', not_in=True)
