from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='example', password='Password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Netfilx", about="#1 Platform", website="http://www.netfilx.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Stream Platform",
            "website": "http://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):

        # create user
        self.user = User.objects.create_user(
            username='example', password='Password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # create stream and watchlist
        self.stream = models.StreamPlatform.objects.create(
            name="Netfilx", about="#1 Platform", website="http://www.netfilx.com")
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream, title="Example Movie", storyline="Example Movie", active=True)

    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Example Story",
            "active": True,
        }
        response = self.client.post(reverse('watchlist-list'), data)
        # if I try to do something that is related to admin, I should get 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(
            # Django reverse() 的 args 參數需要 Tuple 格式，so要加 ,
            reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie')


class ReviewTestCase(APITestCase):
    def setUp(self):

        # create user
        self.user = User.objects.create_user(
            username='example', password='Password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # create stream and watchlist1 2
        self.stream = models.StreamPlatform.objects.create(
            name="Netfilx", about="#1 Platform", website="http://www.netfilx.com")

        # watchlist 1 2是分別獨立的  why要這樣是因為一部電影只能評論一次
        # 1是在測試創review   2是用來測試test_review_update跟test_review_ind的 已經在setUp先創一個先創一個review了
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream, title="Example Movie", storyline="Example Movie", active=True)
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream, title="Example Movie", storyline="Example Movie", active=True)

        # create review (手動先創好 才能測試update等的)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="Great Movie",
                                                   watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        # 一部電影只能評論一次
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_with_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great Movie! - Update",
            "watchlist": self.watchlist,
            "active": False
        }
        response = self.client.put(
            reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(
            reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(
            reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_review_ind_delete(self):
    #     response = self.client.delete(
    #         reverse('review-detail', args=(self.review.id,)))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get(
            '/api/watch/user-reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
