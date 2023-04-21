"""hackportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account import views as acc_views
from account.views import *
from create_hackathon.views import *
from submissions.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signUp', acc_views.signUp, name='signUp'),
    path('login', acc_views.login, name='login'),
    path('hackathon/list', ListHackathonView.as_view()),
    path('hackathon/create', CreateHackathonView.as_view()),
    path('hackathon/register', RegisterHackView.as_view()),
    path('submission/upload', UploadSubmissionView.as_view()),
    path('submission/list', ListSubmissionView.as_view()),
    path('hackathon/registered', ListRegisteredView.as_view()),
]
