from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from create_hackathon.models import CreateHackathon, Registration
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer, Submission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
# Create your views here.

class UploadSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            hackathon_id = request.data['hackathon_id']
            hackathon_obj = CreateHackathon.objects.get(id=hackathon_id)
            registration_object = Registration.objects.get(hackathon=hackathon_obj)
            print(hackathon_obj.submission_type)
            if Submission.objects.filter(author=request.user, hackathon=hackathon_obj).exists():
                return Response({'message':'You have already submitted, Please Edit your submission'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            if not registration_object:
                return Response({'message':'You have not registered in the hackathon'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            if hackathon_obj.submission_type == 'Image':
                sub_obj = Submission.objects.create(registered=registration_object, author=request.user, hackathon=hackathon_obj, 
                                            submission_title=request.data['submission_title'], summary = request.data['summary'] ,
                                            sub_type=hackathon_obj.submission_type, sub_img=request.data['img_file'])
                serialized = SubmissionSerializer(sub_obj, many=True)
                return Response({'message':'Submission successfully submitted','submission':serialized.data}, status=status.HTTP_202_ACCEPTED)

            elif hackathon_obj.submission_type == 'Link':
                sub_obj = Submission.objects.create(registered=registration_object, author=request.user, hackathon=hackathon_obj, 
                                            submission_title=request.data['submission_title'], summary = request.data['summary'] ,
                                            sub_type=hackathon_obj.submission_type, sub_img=request.data['link'])
                serialized = SubmissionSerializer(sub_obj)
                return Response({'message':'Submission successfully submitted','submission':serialized.data}, status=status.HTTP_202_ACCEPTED)

            elif hackathon_obj.submission_type == 'File':
                sub_obj = Submission.objects.create(registered=registration_object, author=request.user, hackathon=hackathon_obj, 
                                            submission_title=request.data['submission_title'], summary = request.data['summary'] ,
                                            sub_type=hackathon_obj.submission_type, sub_img=request.data['file'])                
                serialized = SubmissionSerializer(sub_obj, many=True)
                return Response({'message':'Submission successfully submitted','submission':serialized.data}, status=status.HTTP_202_ACCEPTED)


        except Exception as e:
            return Response({'message':'Submission type invalid',
                             'e': str(e) }, 
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message':'Hackathon does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
class ListSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            sub_obj = Submission.objects.filter(author=user)
            serializer=SubmissionSerializer(sub_obj, many=True)
            return Response({
                'data':serializer.data
            })
        except Exception as e:
            return Response({
                'error':str(e)
            })