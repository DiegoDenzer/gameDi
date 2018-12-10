from django.shortcuts import render
from django.contrib.auth.views import logout_then_login

# Create your views here.

def logout_view(request):
    logout_then_login(request, '')



