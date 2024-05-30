# 미완성

from django import forms

class decrypt_form(forms.Form):
    crypto_image=forms.ImageField()
    key=forms.CharField()
    