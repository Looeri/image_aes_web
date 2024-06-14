from django.shortcuts import render
from imageEncrypt.utils import ImageAES
from .forms import encrypt_form
import os
from django.conf import settings

def index(request):
    if request.method == "POST" :
        form = encrypt_form(request.POST, request.FILES)

        if form.is_valid() :  #입력값을 제대로 넣었을 경우

            aes_module=ImageAES()
            plain_image = form.cleaned_data.get('upload_photo')
            key = form.cleaned_data.get('encrypt_key')
            if key is not None : aes_module.key=key
            profile_checkbox = form.cleaned_data.get('profile_checkbox')
            preview = form.cleaned_data.get('upload_profile_photo') if profile_checkbox else None

            encrypt_dir = os.path.join(settings.MEDIA_ROOT, 'encrypt_images')
            if not os.path.exists(encrypt_dir) : os.makedirs(encrypt_dir)

            encrypt_image_name=aes_module.encrypt(encrypt_dir, plain_image, preview) #이미지 암호화
            print(encrypt_image_name)

            return render(request, "encrypt/CRY.html", {'form':form, 
                                                        'encrypt_image_path':os.path.join(settings.MEDIA_URL, 'encrypt_images', encrypt_image_name),
                                                        'encrypt_image_name':encrypt_image_name})
    else :
        form=encrypt_form()
    return render(request,"encrypt/CRY.html", {'form':form})





