from django.test import TestCase
from .models import CustomUser, Tool
from django.contrib.auth import get_user_model

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', password='password', email='test@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password'))
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_role_default(self):
        self.assertEqual(self.user.role, 'User')

    def test_user_tool_access(self):
        tool = Tool.objects.create(name='Job Tracker')
        self.user.tools.add(tool)
        self.assertTrue(self.user.has_tool_access('Job Tracker'))

class ToolTestCase(TestCase):
    def test_tool_creation(self):
        tool = Tool.objects.create(name='Job Tracker', description='Tracks job applications.')
        self.assertEqual(tool.name, 'Job Tracker')
        self.assertEqual(tool.description, 'Tracks job applications.')
