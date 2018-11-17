import time
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from events.models import Event


class FunctionalTest(LiveServerTestCase):

    def login_user(self, username, password):
        # he fills out & submits signup form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        self.browser.find_element_by_id('id_login_btn').click()

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

    def wait_for_row_in_table(self, row_text):
        MAX_WAIT = 10

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
