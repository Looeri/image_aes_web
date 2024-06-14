#미완성

from django import forms


class encrypt_form(forms.Form):
    upload_photo = forms.ImageField(label='암호화할 이미지 (JPG, PNG, 최대 5MB)',
                                    widget=forms.ClearableFileInput(attrs={'id' : 'upload_photo', 
                                                                           'accept' : 'image/*'}))
    
    encrypt_key = forms.CharField(label='비밀키 입력 (미입력시 기본키 사용)', max_length=20, required=False,
                                  widget=forms.PasswordInput(attrs={'id' : 'encrypt_key', 
                                                                    'placeholder' : "가능한 키 형식: 최대20자, 문자 및 숫자 포함"}))
    
    profile_checkbox = forms.BooleanField(label='프로필 사진 추가', required=False,
                                          widget=forms.CheckboxInput(attrs={'id' : 'profile_checkbox'}))
    
    upload_profile_photo = forms.ImageField(label='프로필 사진 첨부 (JPG, PNG, 최대 5MB)', required=False,
                                            widget=forms.ClearableFileInput(attrs={'id' : 'upload_profile_photo',
                                                                                   'accept' : 'image/*',
                                                                                   'style' : "display: none;"}))

