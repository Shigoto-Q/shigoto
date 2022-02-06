from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("auth/", include("djoser.urls")),
    ]

    def test_create_account(self):
        url = reverse("user-list")
        data = {
            "password": "a2da2dad2a",
            "email": "joey@gmail.com",
            "first_name": "Joey",
            "last_name": "Badass",
            "company": "ERA",
            "zip_code": 1111,
            "city": "vinica",
            "country": "US",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.values()), len(data))

    def test_create_account_fail(self):
        url = reverse("user-list")
        data = {
            "username": "joey",
            "password": "badass",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
