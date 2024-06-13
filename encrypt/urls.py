from django.urls import path
from . import views


app_name='encrypt'
urlpatterns=[
    path('encrypt/result', views.encrypt, name='encrypt'),
    path("encrypt/", views.index, name="index"),
    
]