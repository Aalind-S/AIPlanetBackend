from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateHackathonSerializer, CreateHackathon, RegisterSerializer, Registration
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
# Create your views here.

class CreateHackathonView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            serializer = CreateHackathonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 
                                 'message':'Hackathon has been created!', 
                                 'data':serializer.data})
            return Response({'status':status.HTTP_400_BAD_REQUEST, 
                                'message':'Error', 
                                'data':serializer.errors})
        except Exception as e:
            return Response(
                {'status':status.HTTP_400_BAD_REQUEST, 
                 'message':'Error',
                 'data': str(e)}
            )
        
class RegisterHackView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            hackathon_id = request.data['hackathon_id']
            hackathon_obj = CreateHackathon.objects.get(id=hackathon_id)
            if hackathon_obj.end_date < timezone.now():
                return Response({ 'message':'Hackathon has been concluded'}, status=status.HTTP_400_BAD_REQUEST)
            
            register_obj = Registration.objects.filter(user=user, hackathon=hackathon_obj)

            if len(register_obj)>0:
                return Response({ 'message':'You are already Registered for this Hackathon'}, status=status.HTTP_400_BAD_REQUEST)
            
            register_obj = Registration.objects.create(user=user, hackathon=hackathon_obj)
            serialized = RegisterHackView(register_obj, many=True)
            return Response({ 'message':'You have registered for this Hackathon',
                             'data':serialized.data}, 
                             status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'Hackathon does not exist', 
                             'error': str(e)}, 
                             status=status.HTTP_400_BAD_REQUEST)
        

class ListHackathonView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        try:
            hackathon_query = CreateHackathon.objects.all()
            serializer = CreateHackathonSerializer(hackathon_query, many=True)
            return Response({'status':status.HTTP_200_OK, 
                                'message':'All the hackathons are listed', 
                                'data':serializer.data})
        except Exception as e:
            return Response(
                {'status':status.HTTP_400_BAD_REQUEST, 
                 'message':'Error',
                 'data': str(e)}
            )
        

class ListRegisteredView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            registered_queryset = Registration.objects.filter(user=user)
            serializer = RegisterSerializer(registered_queryset, many=True)
            return Response({
                'message': 'List of All Registered Hackathon',
                'data':serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'message': 'Something went wrong',
                'error':str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
