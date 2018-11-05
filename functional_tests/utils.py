import time
from django.contrib.auth.models import User
from selenium.common.exceptions import WebDriverException
from events.models import Event


def create_user(username, password):
    return User.objects.create_user(
        username=username,
        password=password
    )


def create_event(title, user):
    return Event.objects.create(
        title=title,
        user=user
    )


def wait_for_row_in_table(func_obj, row_text):
    MAX_WAIT = 10

    start_time = time.time()
    # infinite loop
    while True:
        try:
            table = func_obj.browser.find_element_by_id('id_event_table')
            rows = table.find_elements_by_tag_name('tr')
            func_obj.assertIn(row_text, [row.text for row in rows])
            return
        except (AssertionError, WebDriverException) as e:
            # return exception if more than 10s pass
            if time.time() - start_time > 10:
                raise e
            # wait for 0.5s and retry
            time.sleep(0.5)
