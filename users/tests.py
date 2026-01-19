from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_author_create(self):
        url = reverse("users:register")
        data = {
            "password": "1234",
            "email": "test2@sky.pro",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_author_update(self):
        url = reverse("users:user-update", args=(self.user.pk,))
        data = {"country": "Россия"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("country"), "Россия")

    def test_author_delete(self):
        url = reverse("users:user-delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_author_list(self):
        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": 16,
                "email": "test@sky.pro",
                "phone": None,
                "country": None,
                "tg_nick": None,
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
