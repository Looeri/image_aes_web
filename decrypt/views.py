from django.shortcuts import render
from imageEncrypt.utils import ImageAES
from .forms import decrypt_form
import os
from django.conf import settings

def index(request):
    if request.method == "POST" :
        form = decrypt_form(request.POST, request.FILES)

        if form.is_valid() :  #입력값을 제대로 넣었을 경우

            aes_module=ImageAES()
            plain_image = form.cleaned_data.get('upload_photo')
            key = form.cleaned_data.get('Decrypt_key')
            if key is not None : aes_module.key=key

            decrypt_dir = os.path.join(settings.MEDIA_ROOT, 'decrypt_images')
            if not os.path.exists(decrypt_dir) : os.makedirs(decrypt_dir)

            decrypt_image_name=aes_module.decrypt(decrypt_dir, plain_image) #이미지 암호화

            return render(request, "decrypt/DEC.html", {'form':form, 
                                                        'decrypt_image_path':os.path.join(settings.MEDIA_URL, 'decrypt_images', decrypt_image_name),
                                                        'decrypt_image_name':decrypt_image_name})
    else :
        form=decrypt_form()
    return render(request,"decrypt/DEC.html", {'form':form})
