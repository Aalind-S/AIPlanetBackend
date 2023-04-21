from django.db import models
from django.contrib.auth.models import User
from create_hackathon.models import CreateHackathon, Registration
from django.forms import ValidationError
# Create your models here.
from hackportal.constants import SUBMISSIONS
import uuid

class Submission(models.Model):
    # mapping registration and Submission together
    ...
    # for the author we can just registered as the mapper
    # no need of user field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    registered = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='registered')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(CreateHackathon, on_delete=models.CASCADE)
    submission_title = models.CharField(max_length=50, blank=True, null=True)
    summary = models.CharField(max_length=500, blank=True, null=True)
    sub_type = models.CharField(max_length=20, choices=SUBMISSIONS)
    sub_file = models.FileField(upload_to='submission_file', blank=True, null=True)
    sub_img = models.ImageField(upload_to='submission_img', blank=True, null=True)
    sub_link = models.URLField(max_length=500, blank=True, null=True)
    flag = False # to check if it is cleaned or not if its validated

    def clean(self):
        self.flag = True
        # if  wrong submission type then raise an error
        if self.registered.hackathon.submission_type != self.sub_type:
            raise ValidationError("Invalid Submission Type")
        
        if self.sub_type == 'File' and not self.sub_file and (self.sub_img and self.sub_link):
            raise ValidationError("Invalid Submission Type")
        elif self.sub_type == 'Image' and not self.sub_img and (self.sub_file and self.sub_link):
            raise ValidationError("Invalid Submission Type")
        elif self.sub_type == 'Link' and not self.sub_link and (self.sub_file and self.sub_img):
            raise ValidationError("Invalid Submission Type")
        
        super(Submission, self).clean()
    

    def save(self, *args, **kwargs):
        if not self.flag:
            self.full_clean()
        super(Submission, self).save(*args, **kwargs)

