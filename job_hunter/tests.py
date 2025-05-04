from django.test import TestCase
from users.models import CustomUser
from .models import PInfo, Offer, Application, ChatLog
from django.urls import reverse


class PInfoTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="testuser", password="password"
        )
        self.pinfo = PInfo.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            user=user,
        )

    def test_pinfo_creation(self):
        self.assertEqual(self.pinfo.first_name, "John")
        self.assertEqual(self.pinfo.last_name, "Doe")
        self.assertEqual(self.pinfo.email, "john.doe@example.com")
        self.assertEqual(self.pinfo.user.username, "testuser")
