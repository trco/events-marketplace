from django.contrib.auth.models import User
from django.test import TestCase


class SignUpViewTest(TestCase):

    def test_signup(self):
        response = self.client.post(
            '/accounts/signup/',
            data={'username': 'user', 'password': 'test1234'}
        )
        # check if user was created
        self.assertEqual(User.objects.count(), 1)

    def test_redirect_after_post(self):
        response = self.client.post(
            '/accounts/signup/',
            data={'username': 'user', 'password': 'test1234'}
        )
        self.assertRedirects(response, '/accounts/login/')


class AuthenticationViewsTest(TestCase):

    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )
        # login
        self.client.login(username='user', password='test1234')

    def test_login_logout(self):
        response = self.client.get('/')
        # check that the user is logged in
        self.assertEqual(str(response.context['user']), 'user')

        # logout
        response = self.client.logout()
        response = self.client.get('/')
        # check that the user is logged out
        self.assertEqual(str(response.context['user']), 'AnonymousUser')

    def test_login_redirection(self):
        response = self.client.get('/accounts/login/redirection/')
        self.assertRedirects(response, f'/{self.user.username}')
