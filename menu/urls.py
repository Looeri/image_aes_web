from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name="home_redirect"),
    path('home',views.home_index, name="home_index"),
    path('aboutus', views.aboutus_index, name="aboutus_index")
]
