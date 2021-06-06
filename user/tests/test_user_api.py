from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_valid_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {
            'email': 'test@email.com',
            'password': 'mypassword',
            'name': 'DJango Lin'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test user already exists"""
        payload = {
            'email': 'test@email.com',
            'password': 'mypassword',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""

        payload = {
            'email': 'mymail@email.com',
            'password': 'shor'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test a token is created for user"""
        payload = {
            'email': 'test@email.com',
            'password': 'mypassword',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@email.com', password='testpassword')
        payload = {
            'email': 'test@email.com',
            'password': 'mypassword',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exists"""
        create_user(email='test@email.com', password='testpassword')
        payload = {
            'email': 'test@email.com',
            'password': 'mypassword',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_fields(self):
        """Test token creation filed with missing fields in payload"""
        payload = {
            "email": "",
            "password": ""
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Tests api requests that requires authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@email.com',
            password='testpassword',
            name='test name'
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
            })

    def test_post_not_allowed(self):
        """Test that you cannot do a POSt request on the profile"""
        res = self.client.post(ME_URL, {'email': 'email@email.com',
                                        'password': 'testpassword'
                                        })

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_profile_update(self):
        """Test user profile update successsful"""
        payload = {
            'name': 'Paul Shore',
            'password': 'passwordnew',
            'email': 'newemail@email.com'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
