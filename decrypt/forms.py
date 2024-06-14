# 미완성

from django import forms

class decrypt_form(forms.Form):
    upload_photo = forms.ImageField(label='암호화할 이미지 (JPG, PNG, 최대 5MB)',
                                    widget=forms.ClearableFileInput(attrs={'id' : 'upload_photo', 
                                                                           'accept' : 'image/*'}))
    
    encrypt_key = forms.CharField(label='비밀키 입력 (미입력시 기본키 사용)', max_length=20, required=False,
                                  widget=forms.PasswordInput(attrs={'id' : 'Decrypt_key', 
                                                                    'placeholder' : "가능한 키 형식: 최대20자, 문자 및 숫자 포함"}))
    
 