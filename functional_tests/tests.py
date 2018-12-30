from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class SignUpTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_visitor_can_signup_and_login(self):
        # user visits signup page
        self.browser.get(self.live_server_url + '/accounts/signup/')

        # he fills out & submits signup form
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('user_1')
        password_field.send_keys('test1234')
        self.browser.find_element_by_id('id_signup_btn').click()

        # he is redirected to the login page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/accounts/login')

        # he can login with newly created account
        self.login_user('user_1', 'test1234')

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/user_1')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('User profile', header_text)


class CreateEventTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = self.create_user('user_1', 'test1234')

    def tearDown(self):
        self.browser.quit()

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
        self.login_user('user_1', 'test1234')

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
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')
        # he sees created event
        self.wait_for_row_in_table('Test event #1')

        # he visits Add Event page again
        self.browser.get(self.live_server_url + '/events/add')

        # he fills out & submits CreateEvent form once more
        title_field = self.browser.find_element_by_id('id_title')
        title_field.send_keys('Test event #2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')
        # he sees both created events
        self.wait_for_row_in_table('Test event #1')
        self.wait_for_row_in_table('Test event #2')

        # he checks that both events are published at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        # he sees all his published events
        self.wait_for_row_in_table('Test event #1')
        self.wait_for_row_in_table('Test event #2')


class UpdateEventTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_2)

    def tearDown(self):
        self.browser.quit()

    def test_edit_event(self):
        # user visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        self.login_user('user_1', 'test1234')

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        # he sees his events
        self.wait_for_row_in_table('Test event #1')

        # he clicks Edit button to edit event
        self.browser.find_element_by_id('id_edit_link').click()

        # he is redirected to the page with UpdateEvent form
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/edit/{ self.event_1.id }')

        # he updates event
        form_field = self.browser.find_element_by_id('id_title')
        # he clears the field
        form_field.clear()
        form_field.send_keys('Test event #2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        # he sees updated event
        self.wait_for_row_in_table('Test event #2')

        # he checks that event is udpated at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        self.wait_for_row_in_table('Test event #2')

    def test_user_can_edit_only_his_events(self):
        # user visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        self.login_user('user_1', 'test1234')

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        # he sees his events
        self.wait_for_row_in_table('Test event #1')

        # he tries to edit other user's event
        self.browser.get(
            self.live_server_url + f'/events/edit/{ self.event_2.id }'
        )
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/edit/{ self.event_2.id }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('403 Forbidden', page_text)


class DeleteEventTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_1)
        self.event_3 = self.create_event('Test event #3', self.user_2)

    def tearDown(self):
        self.browser.quit()

    def test_delete_event(self):
        # user visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        self.login_user('user_1', 'test1234')

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        # he sees his events
        self.wait_for_row_in_table('Test event #1')
        self.wait_for_row_in_table('Test event #2')

        # he clicks Delete button
        self.browser.find_element_by_id(
            f'id_delete_btn_{ self.event_1.id }'
        ).click()

        # he is redirected to the page for confirmation of deletion
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/events/delete/{ self.event_1.id }')
        # he checks page content
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Confirm deletion', header_text)

        # he clicks Delete button to confirm deletion
        self.browser.find_element_by_id('id_delete_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        # he sees that event was deleted
        self.wait_for_row_in_table('Test event #2')

        # he checks that event was deleted also at index
        self.browser.get(self.live_server_url)
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/')
        self.wait_for_row_in_table('Test event #2')

    def test_user_can_delete_only_his_events(self):
        # user visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        self.login_user('user_1', 'test1234')

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user_1.username }')
        # he sees his events
        self.wait_for_row_in_table('Test event #1')
        self.wait_for_row_in_table('Test event #2')

        # he tries to delete other user's event
        self.browser.get(
            self.live_server_url + f'/events/delete/{ self.event_3.id }'
        )
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/events/delete/{ self.event_3.id }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('403 Forbidden', page_text)


class UniqueProfilesOwnedEventsTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_2)

    def tearDown(self):
        self.browser.quit()

    def test_users_have_unique_profile_with_owned_events(self):
        # user_1 visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        self.login_user('user_1', 'test1234')

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
        self.login_user('user_2', 'test1234')

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
        self.login_user('user_1', 'test1234')

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


class EventDetailsTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Test event #1', self.user)

    def tearDown(self):
        self.browser.quit()

    def test_visit_index_visit_event_details(self):
        # user visits the index page
        self.browser.get(self.live_server_url)

        # he clicks event title to visit event details page
        self.browser.find_element_by_link_text(self.event.title).click()

        # he is redirected to event details page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/events/{ self.event.id }')

        # he checks page content
        event_title = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Test event #1', event_title)


class ManageTicketsTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Test event #1', self.user)

    def tearDown(self):
        self.browser.quit()

    def test_create_ticket(self):
        # user visits login page
        self.browser.get(self.live_server_url + '/accounts/login')
        new_url = self.browser.current_url
        self.assertRegex(new_url, '/accounts/login')

        # he fills out & submits login form
        self.login_user('user', 'test1234')

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{ self.user.username }')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test event #1', page_text)
        self.assertIn('Edit', page_text)
        self.assertIn('Manage Tickets', page_text)

        # he clicks Manage Ticket link
        self.browser.find_element_by_link_text('Manage Tickets').click()

        # he is redirected to the page for managing tickets
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/tickets/{ self.event.id }')
        # he checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(f'Manage Tickets for { self.event.title }', header_text)

        # he fills out & submits CreateTicket form
        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys('Test ticket #1')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # he is redirected to his dedicated profile page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/tickets/{ self.event.id }')

        # he sees created ticket
        self.wait_for_row_in_table('Test ticket #1')
