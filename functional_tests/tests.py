from selenium import webdriver
import unittest


class ExampleTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_example(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.title)
