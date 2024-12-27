from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import models
from . import serializers

class StudentViewset(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer


class RegisteredUsersCount(APIView):
   
    def get(self, request):
        users_count = User.objects.count()  # Count all users in the database
        return Response({"registered_users": users_count})




class UserRegistrationAPIView(APIView):
    serializer_class = serializers.RegistrationSerializer
    # permission_classes = [AllowAny] 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://online-course-rose.vercel.app/Student/active/{uid}/{token}"
            email_subject = "Confirm your email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("https://online-schools.netlify.app/login.html")
    else:
        return redirect("https://online-schools.netlify.app/registetion.html")


class UserLoginApiView(APIView):
    # permission_classes = [AllowAny]
    serializer_class = serializers.UserLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username , password=password)

            if user:

                token,_ = Token.objects.get_or_create(user=user)
                login(request, user)
                print(token.key)
                return Response({"token": token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutApiView(APIView):
    def get(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.ChangePasswordSerializer
    model = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    def get(self, request):
        user = request.user
        serializer = serializers.CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user 
        serializer = serializers.CustomUserSerializer(user, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class IsAdminStatusAPIView(APIView):
    parser_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        user = request.user
        if user.is_staff:
            return Response({"is_admin" : True})
        return Response({"is_admin" : False})