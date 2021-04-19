from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='myemail@email.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def setUp(self):
        '''
        setup the test models
        '''
        self.email = 'johny@gmail.com'
        self.password = '123456'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, password=self.password)

    def test_create_user(self):
        '''
        Test the model creates a user successfully
        '''

        self.assertEqual(self.new_user.email, self.email)
        self.assertTrue(self.new_user.check_password(self.password))
        self.assertTrue(get_user_model().objects.exists())

    def test_email_normalized(self):
        '''
        Test email was normalized
        '''
        email = "mytest@MYDOMAIN.COM"
        password = "testpasswords"
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''
        Test user creation with invalid email
        '''
        email = None
        password = "mytestpassword"
        # user = get_user_model().objects.create(email=email,
        #                                     password = password)
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=email,
                                                 password=password)

    def test_create_super_user(self):
        """Test super user creation successfully"""
        user = get_user_model().objects.create_superuser(
                email="mymail@,ail.com", password="mypasswod")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag strinmg representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test ingredients string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumuber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_converting_recipe_object_to_string(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and muchroom asuce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
