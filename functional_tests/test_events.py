from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class CreateEventTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = self.create_user('user', 'test1234')

    def test_visit_index_visit_add_event_create_event_visit_index(self):
        # user visits the index page
        self.browser.get(self.live_server_url)

        # user checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Events Marketplace', header_text)

        # user clicks Add Event link
        self.browser.find_element_by_link_text('Add Event').click()

        # user is redirected to login
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/accounts/login')

        # user fills out & submits login form
        self.login_user('user', 'test1234')

        # user is redirected to the page with CreateEvent form
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/events/add')

        # user checks page content
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Event', header_text)

        # user fills out & submits CreateEvent form
        title_field = self.browser.find_element_by_id('id_title')
        title_field.send_keys('Event 1')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # user is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')

        # user sees created event
        self.wait_for_text_in_body('Event 1')

        # user visits Add Event page again
        self.browser.get(self.live_server_url + '/events/add')

        # user fills out & submits CreateEvent form once more
        title_field = self.browser.find_element_by_id('id_title')
        title_field.send_keys('Event 2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # user is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')

        # user sees both created events
        self.wait_for_text_in_body('Event 1', 'Event 2')

        # user checks that both events are published at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')

        # user sees all his published events
        self.wait_for_text_in_body('Event 1', 'Event 2')


class UpdateEventTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Event 1', self.user_1)
        self.event_2 = self.create_event('Event 2', self.user_2)

    def test_edit_event_can_edit_only_owned_events(self):
        # user_1 logs in
        self.login_user('user_1', 'test1234', self.user_1)

        # user_1 sees his events at his profile page
        self.wait_for_text_in_body('Event 1')

        # user_1 clicks Edit button to edit event
        self.browser.find_element_by_id('id_edit_link').click()

        # user_1 is redirected to the page with UpdateEvent form
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/edit/{ self.event_1.id }')

        # user_1 updates event
        form_field = self.browser.find_element_by_id('id_title')
        form_field.clear()
        form_field.send_keys('Event 2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # user_1 is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')

        # user_1 sees updated event
        self.wait_for_text_in_body('Event 2')

        # user_1 checks that event is udpated at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        self.wait_for_text_in_body('Event 2')

        # user_1 tries to edit other user's event
        self.browser.get(
            self.live_server_url + f'/events/edit/{ self.event_2.id }'
        )
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/edit/{ self.event_2.id }')
        self.wait_for_text_in_body('403 Forbidden')


class DeleteEventTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Event 1', self.user_1)
        self.event_2 = self.create_event('Event 2', self.user_1)
        self.event_3 = self.create_event('Event 3', self.user_2)

    def test_delete_event_can_delete_only_owned_events(self):
        # user_1 fills out & submits login form
        self.login_user('user_1', 'test1234', self.user_1)

        # user_1 sees his events
        self.wait_for_text_in_body('Event 1', 'Event 2')

        # user_1 clicks Delete button
        self.browser.find_element_by_id(
            f'id_delete_btn_{ self.event_1.id }'
        ).click()

        # user_1 is redirected to the page for confirmation of deletion
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/events/delete/{ self.event_1.id }')

        # user_1 checks page content
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Confirm deletion', header_text)

        # user_1 clicks Delete button to confirm deletion
        self.browser.find_element_by_id('id_delete_btn').click()

        # user_1 is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        self.wait_for_text_in_body('Event 2')
        self.wait_for_text_in_body('Event 1', not_in=True)

        # user_1 checks that event was deleted also at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        self.wait_for_text_in_body('Event 1', not_in=True)

        # user_1 tries to delete other user's event
        self.browser.get(
            self.live_server_url + f'/events/delete/{ self.event_3.id }'
        )
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/delete/{ self.event_3.id }')
        self.wait_for_text_in_body('403 Forbidden')


class EventDetailsTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Event 1', self.user)

    def test_visit_index_visit_event_details(self):
        # user visits the index page
        self.browser.get(self.live_server_url)

        # user clicks event title to visit event details page
        self.browser.find_element_by_link_text(self.event.title).click()

        # user is redirected to event details page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/events/{ self.event.id }')

        # user checks page content
        event_title = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Event 1', event_title)
