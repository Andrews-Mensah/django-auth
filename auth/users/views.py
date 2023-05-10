from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import jwt, datetime



# from auth.users.models import User

from .serializers import UserSerializer

# Create your views here.

class RegisterView(APIView):
    def post(self, request):

        data = request.data
        hash_password = make_password(data.get('password'))
        data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'password': hash_password
        }

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        return Response(data= serializer.data, status= status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']


        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        

        if not user and check_password (password, user.password):
            raise AuthenticationFailed('Incorrect password')
        
        id = str(user.id)
        
        payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='access-token', value=token, httponly=True)

        response.data = {
            'access-token': token,
            'message': "Success"
        }
        
        return response
    



class UserView(APIView):
    def get (self, request):
        token = request.COOKIES.get('access-token')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)


        return Response(serializer.data)
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access-token')

        response.data = {
            'message': 'success'
        }

        return response



  


        
