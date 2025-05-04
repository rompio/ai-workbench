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


class OfferTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="testuser", password="password"
        )
        self.offer = Offer.objects.create(
            position="Software Engineer", company="TechCorp", user=user
        )

    def test_offer_creation(self):
        self.assertEqual(self.offer.position, "Software Engineer")
        self.assertEqual(self.offer.company, "TechCorp")

    def test_offer_str(self):
        self.assertEqual(str(self.offer), "Software Engineer at TechCorp")


class ApplicationTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="testuser", password="password"
        )
        offer = Offer.objects.create(
            position="Software Engineer", company="TechCorp", user=user
        )
        self.application = Application.objects.create(
            resume="Resume content", user=user, offer=offer
        )

    def test_application_creation(self):
        self.assertEqual(self.application.resume, "Resume content")
        self.assertEqual(self.application.user.username, "testuser")
        self.assertEqual(self.application.offer.position, "Software Engineer")

    def test_application_str(self):
        self.assertEqual(
            str(self.application),
            "Application by testuser for Software Engineer",
        )

