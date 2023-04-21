from rest_framework import serializers
from create_hackathon.models import CreateHackathon, Registration

class CreateHackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateHackathon
        fields = '__all__'
        #ordering = ['created_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
