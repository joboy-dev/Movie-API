from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .api import serializers, views
from . import models

# StreamPlatform testcase
class StreamPlatformTestCase(APITestCase):

    def setup(self):
        # create a user
        self.user = User.objects.create_user(username='example', password='password123')
        # access a token for the user
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='Top streaming platform', website='https://netflix.com')

    def test_streamplatform_create(self):
        # set data  to be sent to db by the user. the user should be an admin to do this though
        data = {
            # from models
            "name":"Netflix",
            "about":"#1 Streaming platform",
            "website":"https://netflix.com"
        }

        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_update(self):
        # set data  to be sent to db by the user. the user should be an admin to do this though
        data = {
            # from models
            "name":"Netflix",
            "about":"#1 Streaming platform",
            "website":"https://netflix.com"
        }

        response = self.client.put(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_streamplatform_delete(self):
        # set data  to be sent to db by the user. the user should be an admin to do this though
        data = {
            # from models
            "name":"Netflix",
            "about":"#1 Streaming platform",
            "website":"https://netflix.com"
        }

        response = self.client.delete(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_streamplatform_get(self):
        response = self.client.get(reverse('streamplatform-list')) # no need to pass data since it is a get request
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

