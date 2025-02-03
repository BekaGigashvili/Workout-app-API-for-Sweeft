from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
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
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            access = request.data.get('access')
            
            if not refresh or not access:
                return Response({
                    'message': 'refresh and acces tokens are required.',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken(refresh)
            refresh.blacklist()

            access = RefreshToken(access)
            access.blacklist()

            return Response({
                'message': 'Successfully loggeed out.',
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Invald token.',
            }, status=status.HTTP_400_BAD_REQUEST)