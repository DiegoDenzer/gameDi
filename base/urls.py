from django.urls import path

from base.views import PersonagensView
from . import views

urlpatterns = [
    path('', views.logout_view , name='logout'),
    path('personagens', PersonagensView.as_view(), name='personagens')
]