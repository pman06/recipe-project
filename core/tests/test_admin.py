from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@email.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='testmail@email.com',
            password='passwordtotest',
            name='John Doe'
        )

    def test_users_created(self):
        '''Test that users are listed on users page'''
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)
        self.assertTrue(get_user_model().objects.exists())

        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.name)

    def test_user_change(self):
        '''Test the user edit page works'''
        url = reverse('admin:core_user_change', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
