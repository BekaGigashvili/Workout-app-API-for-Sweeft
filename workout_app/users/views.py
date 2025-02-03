from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login was successful', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ))
        },
        operation_description="Log in user by provided email and password. returns refresh and access tokens provided by jwt and a message indicating successful login, or error code and message otherwise."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data['email']
        password=serializer.validated_data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            'refresh': str(refresh),
            'access': access,
            'message': 'Success!',
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            responses={
                200: 'Successfully logged out!',
                400: 'Invalid token.'
            },
            operation_description="Logout the user by invalidating the refresh token."
    )
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            
            if not refresh:
                return Response({
                    'message': 'refresh token is required.',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken(refresh)
            refresh.blacklist()

            return Response({
                'message': 'Successfully logged out.',
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Invald token.',
            }, status=status.HTTP_400_BAD_REQUEST)