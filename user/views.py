from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
<<<<<<< HEAD
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES
=======
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
>>>>>>> 355dca2 (Added endpoint for creating and authenticating users)
