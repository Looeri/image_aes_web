from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from imageEncrypt.utils import ImageAES, Menu
from .forms import encrypt_form

@require_http_methods(["GET"])
def index(request):
    return render(request,"CRY.html")

#위에 @require_http_methods(['GET', 'POST'])로 안전성을 높일 수 있다
menu=Menu()
        



@require_http_methods(["POST"])
def encrypt(request):
    if request.method == 'POST' :
        form = encrypt_form(request.POST, request.FILES)

        if form.is_valid() :  #입력값을 제대로 넣었을 경우
            aes_module=ImageAES()
            if 'key' in request.POST : aes_module.key=request.POST.get('key')  # 이용자 지정 암호가 있다면 그걸 사용한다

            crypto_image=aes_module.encrypt(request.FILES.get('plain_image'), request.FILES.get('preview')) #이미지 암호화

            return render(request, "CRY.html", {"crypto_image":crypto_image})

        
        else : # 사용자가 이미지, 암호 등에서 사이트가 지정하지 않은 형태로 입력했을 때
            return render(request, "CRY.html", context={'form':form}, content_type="multipart/form-data")   # 오류가 난 항목에 대해 알리면서 원래 화면이 렌더된다
        
    else: redirect("encrypt:index")



