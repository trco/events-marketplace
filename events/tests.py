from django.test import TestCase


class HomePageTest(TestCase):
    def test_index_visit(self):
        response = self.client.get('/')
        self.assertContains(response, 'Events Marketplace')
        self.assertContains(response, 'Add Event')

    def test_add_event_click(self):
        response = self.client.get('/events/add')
        self.assertContains(response, 'Add Event')
