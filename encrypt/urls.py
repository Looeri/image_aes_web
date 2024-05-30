from django.urls import path
from . import views


app_name='encrypt'
urlpatterns=[
    path('encrypt/result', views.encrypt, name='encrypt'),
    path("encrypt/", views.index, name="index"),
    
    path('home/',views.menu.go_home, name="go_home"),
    path('encrypt/', views.menu.go_encrypt, name="go_encrypt"),
    path('decrypt/', views.menu.go_decrypt, name="go_decrypt"),
    path('about-us/', views.menu.go_aboutus, name="go_aboutus")
]