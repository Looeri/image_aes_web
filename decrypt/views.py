from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from imageEncrypt.utils import ImageAES
from forms import decrypt_form

# Create your views here.

@require_http_methods(["GET"])
def index(request):
    return render(request, template_name="index.html")

@require_http_methods(["POST"])
def decrypt(request):
    form=decrypt_form(request.POST, request.FILE)

    if form.is_valid() :
        aes_module=ImageAES()
        if 'key' in request.POST : aes_module.key=request.POST.get('key')

        plain_image=aes_module.decrypt(request.FILES.get('crypto_image'))
        return render(request, "html 이름", context={"plain_image":plain_image}, content_type="multipart/from-data")

    else :
        return render(request, "html 이름", context={'form':form})


def go_encrypt(request):
    return redirect("encrypt:index")

    
