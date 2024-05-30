from django.urls import path
from . import views


app_name='decrypt'
urlpatterns=[
    path("decrypt/", views.index, name='index'),
    path('encrypt', views.go_encrypt, name="go_encrypt")
    
]