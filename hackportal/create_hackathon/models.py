from django.db import models
import uuid
from django.contrib.auth.models import User
import datetime as dt
from hackportal.constants import SUBMISSIONS
# Create your models here.

class CreateHackathon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.TextField()
    created_at = models.DateTimeField(default = dt.datetime.now)
    hackathon_img = models.ImageField(upload_to='images',blank=True, null=True)
    background_img = models.ImageField(upload_to='images', blank=True, null=True)
    submission_type = models.CharField(max_length=30, choices=SUBMISSIONS)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(CreateHackathon, on_delete=models.CASCADE, related_name='hackathon')