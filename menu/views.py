from django.shortcuts import redirect, render
from django.views import View

# Create your views here.

'''class Menu(View):


    @require_http_methods(["GET"])
    @staticmethod
    def go_home(request):
        if request.GET.get(['redirect']) == 'home':
            return redirect('home:index')

    @require_http_methods(["GET"])
    @staticmethod
    def go_encrypt(request):
        if request.GET.get(['redirect'])=='encrypt':
            return redirect('encrypt:index')

    @require_http_methods(["GET"])
    @staticmethod
    def go_decrypt(request):
        if request.GET.get('redirect')=="decrypt":
            return redirect('decrypt:index')

    @require_http_methods(["GET"])
    @staticmethod       
    def go_aboutus(request):
        if request.GET.get(['redirect'])=='aboutus':
            return redirect('aboutus:index')'''
def home_redirect(request):
    return redirect("home_index")

def home_index(request):
    return render(request, "texts/home.html")

def aboutus_index(request):
    return render(request, "texts/me.html")