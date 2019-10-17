"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic.base import TemplateView

### MOVE THIS STUFF IF THIS EXPERIMENT IS KEPT
from rest_framework.views import APIView
from rest_framework.response import Response 

class UserView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"username": request.user.username})
        else: 
            return Response({"username": "Anonymous"})

###

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name="registration/profile.html"), name="profile"),
    path('record/', include('cleanslate.urls')),
    path('api/users/', UserView.as_view())
]
