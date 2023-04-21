from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from account.serializer import SignUpSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Create your views here.
# User model contains username email password password2


@api_view(['POST'])
def signUp(request):
    try:
        username = request.data['username']
        #email = request.data['email']
        password = request.data['password']

        #if User.objects.filter(email=email).exists():
            #return Response({'message':'Email already exists'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'message':'Username already exists'},status=status.HTTP_400_BAD_REQUEST)
        else:

            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid()
            user_obj = User.objects.create(username=username, password=password)
            
            user_obj.save()
            user = User.objects.get(username=username)
            tokenRef = RefreshToken.for_user(user)
            return Response({
                'message': 'The account has been created',
                'refresh': str(tokenRef),
                'access': str(tokenRef.access_token),
            }, 
            status = status.HTTP_201_CREATED)
        
            #else:
                #return Response({'message':'Serializer not valid'},status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message':'Fill the details correctly'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        return Response({"message":"Fill the details correctly"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    usr_obj = User.objects.get(username=username)
    if not usr_obj:
        return Response({"message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    if password != usr_obj.password:
        return Response({"message":"Wrong or Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        #auth_login(request, user)
        tokenRef = RefreshToken.for_user(usr_obj)
        #serializer = SignUpSerializer(usr_obj)
        return Response({"message": "You have logged in",
                    
                    'refresh':str(tokenRef),
                    'access':str(tokenRef.access_token)},
                status = status.HTTP_200_OK)

"""    user = authenticate(username=username, password=password) # returns a user object if valid elese returns None
    if user:
        tokenRef = RefreshToken.for_user(usr_obj)
        #serializer = SignUpSerializer(usr_obj)
        return Response({"message": "You have logged in",
                    
                    'refresh':str(tokenRef),
                    'access':str(tokenRef.access_token)},
                status = status.HTTP_200_OK) """