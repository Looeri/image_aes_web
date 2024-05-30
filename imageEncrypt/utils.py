from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import numpy as np
import cv2 as cv
from django.views import View
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

#이미지 암호화, 복호화 클래스
class ImageAES():
    def __init__(self, key=None):
        self.iv=b'Z%$\xec\xe1Y\x894\x88\xa8\xb7\x08\xd0\xdb\xb2\r' #16byte의 iv(초기화 벡터)
        
        if key=="Hello Password!" : key=key+" this is key."  #사용자가 암호 입력하지 않으면 사용하는 암호. 암호를 감추기 위해 위에 바로 안적음.
        self.key=SHA256.new(key.encode('utf-8')).digest()

        self.aes=AES.new(self.key, AES.MODE_CBC, self.iv)
        
    def encrypt(self, plain_image_path, preview_path=None):
        pimage_path=np.fromfile(plain_image_path,np.uint8)  #이미지명이 한글이면 오류가 잘 생긴다고 해서 경로를 바꿔서 불렀다
        pimage=cv.imdecode(pimage_path,cv.IMREAD_COLOR) 
        pimage_height, pimage_width, color=pimage.shape      # 이미지를 Mat 클래스로 가져온다. shape=(height, width, 3)이다
                                            # 16바이트(128bit)씩 암호화 가능 : 어지간하면 패딩이 필요함


        #프리뷰 사진이 존재한다면(프리뷰 데이터 가져오기 및 비율 조정)
        if preview_path!=None:  
            ppath=np.fromfile(preview_path,np.uint8)   #프리뷰명이 한글이면 오류나니 경로 바꿔 부름 2
            preview=cv.imdecode(ppath,cv.IMREAD_COLOR)
            preview_height, preview_width =preview.shape[:2]

            #프리뷰를 합치기 위해 가로 길이를 원본 사진과 동일하게 맞추는 중(세로는 프리뷰의 가로x세로 비율대로 바뀜)
            preview_ratio= pimage_width / preview_width
            preview_width=pimage_width
            preview_height= int(preview_height*preview_ratio)

            preview.resize((preview_height, preview_width))  # 프리뷰와 암호화할 사진의 가로 길이가 같아짐


        #이미지 패딩하기
        pad_height= ((pimage_height*pimage_width)-1)%16+1   #1~16값을 가짐 (복호화 시 높이를 알기 위해 직접 패딩함)
        pad_image=np.vstack(np.zeros(pad_height,preview_width,color),pimage)   #위는 이미지 패딩, 아래는 원본 이미지가 들어간다

        height_2=bin(pimage_height)[2:]  #패딩 공간중 제일 앞(0,0)에 iheight를 적어놓음(숫자가 256까지 들어가서 1바이트 단위로  나눠서 들어가게 함. 복호화 대비용)
        
        chnum=1
        while len(pimage_height)<chnum*8 :
            pad_image[0,0,3-chnum]+=int("0o"+height_2[-8+(chnum-1)*-8:(chnum-1)*-8])
            chnum+=1
        pad_image[0,0,3-chnum]+=int("0o"+height_2[:(chnum-1)*-8])
        pad_image[0,1,3]+=pad_height  #두번째 px(0,1)에 패딩 높이를 적어놓는다

        crypto_data=self.aes.encrypt(pad_image)
        #이후 복호화를 위해 암호화 된 이미지를 위아래로 뒤집는다. 
        crypto_image=np.flipud(np.frombuffer(crypto_data, dtype=np.uint8).reshape(pimage_height+pad_height,pimage_width,color))

        # 프리뷰가 존재하면 암호화된 이미지 세로로 병합(위가 프리뷰, 아래가 암호화 이미지). np.concatenate((합칠 배열들), axis=0)도 
        # 같은 결과라고 하니 어느게 더 빠른지 실험해 볼 것
        if preview_path!=None:
            crypto_image=np.vstack((preview, crypto_image))

        return crypto_image



    def decrypt(self, crypto_image_path):
        cimage_path=np.fromfile(crypto_image_path,np.uint8)  #이미지명이 한글이면 오류가 잘 생긴다고 해서 경로를 바꿔서 불렀다
        cimage=cv.imdecode(cimage_path,cv.IMREAD_COLOR) 
        cimage_height, cimage_width, color=cimage.shape      # 이미지를 Mat 클래스로 가져온다. shape=(height, width, 3)이다

        #암호화 한 데이터를 뒤집어 저장했으니 다시 뒤집어 복호화한다
        encrypt_data=self.aes.decrypt(np.flipud(cimage))  #위 원본데이터 아래 복호화에 영향받은 프리뷰(어차피 짜를거라 상관없음)
        encrypt_image=np.frombuffer(encrypt_data, dtype=np.uint8).reshape(cimage_height, cimage_width, color)

        #원본높이, 패딩높이 찾기(암호화할 때 패딩의 제일 앞 1px(3byte)는 원본 높이, 나머지는 0으로 채웠다 )
        pimage_height=encrypt_image[0,0,:]
        pimage_height=int(bin(pimage_height[0])+bin(pimage_height[1])[2:]+bin(pimage_height[2])[2:],0)  #원본 이미지의 높이
        pad_height=encrypt_image[0,1,3] #패딩의 높이
        
        plain_image=encrypt_image[pad_height:pimage_height,...]   # 패딩, 프리뷰(있다면)이 이과정에서 잘린다. 
        return plain_image

#views.py에서 공통으로 사용할 메뉴 클릭시 redirect()하는 클래스
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
    @require_http_methods(["GET"])
    def go_decrypt(request):
        if request.GET.get('redirect')=="decrypt":
            return redirect('decrypt:index')

    @staticmethod       
    def go_aboutus(request):
        if request.GET.get(['redirect'])=='aboutus':
            return redirect('aboutus:index')




        


        

        
