from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        # this is going to send a request to this link(register) with this data.
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='example', password='NewPassword@123')

    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="example")

        # 就像登入一樣   #Authorization: Token abcd1234efgh5678
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # 之後，任何 self.client.get() 或 self.client.post() 之類的請求，都會自動包含這個 Authorization 標頭。

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
