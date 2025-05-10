from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.
class ProfileTestCase(TestCase):
    def test_profile_redirect(self):
        user = User.objects.create_user('testuser')
        self.client.force_login(user)
        response = self.client.get(reverse('my-profile'))
        self.assertRedirects(response, reverse('profile', args=['testuser']))