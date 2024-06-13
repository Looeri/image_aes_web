#미완성

from django import forms


class encrypt_form(forms.Form): # request에서 들어올 데이터 종류
    upload_photo=forms.ImageField(allow_empty_file=False,
                                 error_messages={"required":"해당 항목은 필수입니다."} ) #암호화 해야 하는 이미지
    key=forms.CharField( initial="Hello Password!", min_length=4,
                        error_messages={"min_length":"암호의 길이가 너무 짧습니다"}) #암호화할 키(없을시 initial값이 초기값이 됨)
    preview=forms.ImageField(allow_empty_file=True) #암호화된 이미지 위에 붙일 이미지(없을수도 있음)

