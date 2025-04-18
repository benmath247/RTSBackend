from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model, authenticate, login
import logging
from .serializers import UserSerializer
from django.contrib.auth import logout

logger = logging.getLogger(__name__)
User = get_user_model()

class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        logger.debug(f"Current user: {self.request.user}")

        if self.request.user.is_authenticated:
            try:
                return User.objects.get(email=self.request.user.email)
            except User.DoesNotExist:
                self.permission_denied(self.request, message="User not found")
        self.permission_denied(self.request, message="Not authenticated")

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer

class EditUserView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=200)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)

