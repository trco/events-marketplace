from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ManageTicketsTest(FunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Event 1', self.user_1)
        self.event_2 = self.create_event('Event 2', self.user_2)
        # create tickets
        self.ticket_1 = self.create_ticket('Ticket 1', self.event_1)
        self.ticket_2 = self.create_ticket('Ticket 2', self.event_2)

    def test_create_ticket(self):
        # user_1 fills out & submits login form
        self.login_user('user_1', 'test1234', self.user_1)

        # user_1 checks page content
        self.wait_for_text_in_body(
            'Event 1', 'Ticket 1', 'Edit', 'Manage Tickets'
        )

        # user_1 clicks Manage Tickets link
        self.browser.find_element_by_link_text('Manage Tickets').click()

        # user_1 is redirected to the page for managing tickets
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/tickets/{self.event_1.id}')

        # user_1 checks page content
        self.assertIn('Events Marketplace', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(f'Manage Tickets for {self.event_1.title}', header_text)

        # user_1 fills out & submits CreateTicket form
        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys('Ticket 2')
        submit_btn = self.browser.find_element_by_id('id_submit_btn').click()

        # user_1 is redirected to dedicated event tickets page
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/tickets/{self.event_1.id}')

        # user_1 sees created ticket
        self.wait_for_text_in_body('Ticket 2')

        # user_1 checks if created ticket is visible at his profile page
        self.browser.get(self.live_server_url + '/user_1')
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/{self.user_1.username}')
        self.wait_for_text_in_body('Event 1', 'Ticket 1', 'Ticket 2')

    def test_delete_ticket_can_delete_only_owned_tickets(self):
        # user_1 fills out & submits login form
        self.login_user('user_1', 'test1234', self.user_1)

        # user_1 sees his event and ticket
        self.wait_for_text_in_body('Event 1', 'Ticket 1')

        # user_1 clicks Manage Ticket link
        self.browser.find_element_by_link_text('Manage Tickets').click()

        # user_1 is redirected to the page for managing tickets
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/tickets/{self.event_1.id}')

        # user_1 clicks Delete button next to the ticket
        self.browser.find_element_by_id(
            f'id_delete_btn_{self.ticket_1.id}'
        ).click()

        # user_1 is redirected to the page for confirmation of deletion
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, f'/tickets/delete/{self.ticket_1.id}')

        # user_1 checks page content
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Confirm deletion', header_text)

        # user_1 clicks Delete button to confirm deletion
        self.browser.find_element_by_id('id_delete_btn').click()

        # user_1 is redirected to the page for managing tickets
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/tickets/{self.event_1.id}')

        # user_1 checks that ticket was deleted also at his profile page
        self.browser.get(self.live_server_url + f'/{self.user_1.username}')
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'{self.user_1.username}')

        # user_1 sees his event without ticket
        self.wait_for_text_in_body('Event 1')
        self.wait_for_text_in_body('Ticket 1', not_in=True)

        # user_1 tries to delete other user's ticket
        self.browser.get(
            self.live_server_url + f'/tickets/delete/{self.ticket_2.id}'
        )
        new_url = self.browser.current_url
        self.assertRegex(new_url, f'/tickets/delete/{self.ticket_2.id}')
        self.wait_for_text_in_body('403 Forbidden')
