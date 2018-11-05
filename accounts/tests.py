from django.contrib.auth.models import User
from django.test import TestCase


class SignUpViewTest(TestCase):

    def test_signup(self):
        response = self.client.post(
            '/accounts/signup/',
            data={'username': 'user_1', 'password': 'test1234'}
        )
        # check if user was created
        self.assertEqual(User.objects.count(), 1)

    def test_redirect_after_post(self):
        response = self.client.post(
            '/accounts/signup/',
            data={'username': 'user_1', 'password': 'test1234'}
        )
        self.assertRedirects(response, '/accounts/login/')
