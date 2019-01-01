import time
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from events.models import Event
from tickets.models import Ticket


class FunctionalTest(LiveServerTestCase):

    # basic setUp & tearDown
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login_user(self, username, password, user=None):
        if user is not None:
            self.browser.get(self.live_server_url + '/accounts/login')
            login_url = self.browser.current_url
            self.assertRegex(login_url, '/accounts/login')

        # user fills out & submits login form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        self.browser.find_element_by_id('id_login_btn').click()

        if user is not None:
            # user is redirected to his dedicated profile page
            redirect_url = self.browser.current_url
            self.assertRegex(redirect_url, f'/{ user.username }')

    def create_user(self, username, password):
        return User.objects.create_user(
            username=username,
            password=password
        )

    def create_event(self, title, user):
        return Event.objects.create(
            title=title,
            user=user
        )

    def create_ticket(self, name, event):
        return Ticket.objects.create(
            name=name,
            event=event
        )

    def wait_for_text_in_body(self, *args, not_in=None):
        MAX_WAIT = 10

        start_time = time.time()
        # infinite loop
        while True:
            try:
                body = self.browser.find_element_by_tag_name('body')
                body_text = body.text
                # check that text is in body
                if not not_in:
                    for arg in args:
                        self.assertIn(arg, body_text)
                # check there is no text in body
                else:
                    for arg in args:
                        self.assertNotIn(arg, body_text)
                return
            except (AssertionError, WebDriverException) as e:
                # return exception if more than 10s pass
                if time.time() - start_time > MAX_WAIT:
                    raise e
                # wait for 0.5s and retry
                time.sleep(0.5)
