from django.shortcuts import redirect
from django.views import View

# Create your views here.

class Menu(View):

    @staticmethod
    def go_home(request):
        if request.GET.get(['redirect']) == 'home':
            return redirect('home:index')

    @staticmethod
    def go_encrypt(request):
        if request.GET.get(['redirect'])=='encrypt':
            return redirect('encrypt:index')

    @staticmethod
    def go_decrypt(request):
        if request.GET.get('redirect')=="decrypt":
            return redirect('decrypt:index')

    @staticmethod       
    def go_aboutus(request):
        if request.GET.get(['redirect'])=='aboutus':
            return redirect('aboutus:index')