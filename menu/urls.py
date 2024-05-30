from django.urls import path
from .views import Menu

urlpatterns = [
    path('menu/home',Menu.go_home, name="go_home"),
    path('menu/encrypt', Menu.go_encrypt, name="go_encrypt"),
    path('menu/decrypt', Menu.go_decrypt, name="go_decrypt"),
    path('menu/aboutus', Menu.go_aboutus, name="go_aboutus")
]
