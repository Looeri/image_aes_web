from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import numpy as np
import cv2 as cv
import os
import time
from PIL import Image
from io import BytesIO

#이미지 암호화, 복호화 클래스
class ImageAES():
    #<------------- !!!!!! 중요 !!!!!!!! ------------------>
    #이미지 저장시 png, 그중에서도 무손실 압축 방식으로 저장하게 할 것(암호화한 이미지만이라도)
    #imwrite로 저장시 [cv.IMWRITE_PNG_COMPRESSION,0]으로
    #불러올 때도 cv.IMREAD_UNCHANGED로 불러오자!
    #이미지가 조금이라도 변형되면 복호화가 안된다!!!!!!

    def __init__(self, key=""):
        self.iv=b'Z%$\xec\xe1Y\x894\x88\xa8\xb7\x08\xd0\xdb\xb2\r' #16byte의 iv(초기화 벡터)


        #key 만들기
        self.key=key
        if self.key=="" : self.key=self.key+" this is key."  #사용자가 암호 입력하지 않으면 사용하는 암호. 암호를 감추기 위해 위에 바로 안적음.
        self.key=SHA256.new(self.key.encode('utf-8')).digest()

        self.aes=AES.new(self.key, AES.MODE_CBC, self.iv)
        
        
    #암호화 함수, 사진 경로(그리고 이미지가 저장될 경로)를 입력하면 암호화된 이미지가 저장되고 그 경로가 출력됨.
    def encrypt(self, save_dir, plain_image, preview=None):
        #원본 이미지 불러오기, 크기 측정
        pdata=plain_image.read()
        pil_pimage=Image.open(BytesIO(pdata))
        pimage=np.array(pil_pimage.convert('RGB'))[:,:,::-1]            #사용자에게서 받아온 이미지를 저장하지 않고 views에서 줄 수 있어서 바로 받아오기로 함
        pimage_height, pimage_width, color=pimage.shape      # 이미지를 Mat 클래스로 가져온다. shape=(height, width, 3)이다
        pimage_name=os.path.splitext(plain_image.name)[0]
        
        print(pimage[0,0,:])

        #이미지 패딩하기(AES 블록 크기(16bytes, 128bit) 맞추기 + 복호화를 위한 높이값 저장)
        pad_height= 16-(pimage_height%16)   #1~16값을 가짐 (복호화 시 높이를 알기 위해 직접 패딩함)
        pad_height = 16 if pad_height == 0 else pad_height
        pad_image=np.vstack((np.zeros((pad_height,pimage_width,color), dtype=np.uint8),pimage))   #위는 이미지 패딩, 아래는 원본 이미지가 들어간다

        height_2=bin(pimage_height)[2:]  #패딩 공간중 제일 앞(0,0)에 iheight를 적어놓음(숫자가 256까지 들어가서 1바이트 단위로  나눠서 들어가게 함. 복호화 대비용)
        if len(height_2)<=8:
            pad_image[0,0,2]+=int(height_2, 2)
        elif len(height_2)>8 and len(height_2)<=16 :
            pad_image[0,0,2]+=int(height_2[-8:],2)
            pad_image[0,0,1]+=int(height_2[:-8],2)
        else :
            pad_image[0,0,2]+=int(height_2[-8:],2)
            pad_image[0,0,1]+=int(height_2[-16:-8],2)
            pad_image[0,0,0]+=int(height_2[:-16],2)
        pad_image[0,1,2]+=pad_height  #두번째 px(0,1)에 패딩 높이를 적어놓는다

        print(pad_image[0,0,:])

        #이미지 암호화 및 복호화 대비(상하반전)
        crypto_data=self.aes.encrypt(pad_image.tobytes()) 
        crypto_image=np.frombuffer(crypto_data, dtype=np.uint8).reshape(pimage_height+pad_height,pimage_width,color)
        crypto_image=np.flipud(crypto_image)

        #프리뷰 사진이 존재한다면(프리뷰 이미지 가져오기 및 비율 조정)
        if preview != None:  
            #ppath=np.fromfile(preview,np.uint8)   #프리뷰명이 한글이면 오류나니 경로 바꿔 부름 2
            #preview=cv.imdecode(ppath,cv.IMREAD_UNCHANGED)
            predata=preview.read()
            pil_preimage=Image.open(BytesIO(predata))
            preview=np.array(pil_preimage.convert('RGB'))[:,:,::-1]
            preview_height, preview_width =preview.shape[:2]

            #프리뷰를 합치기 위해 가로 길이를 원본 사진과 동일하게 맞추는 중(세로는 프리뷰의 가로x세로 비율대로 바뀜)
            preview_ratio= pimage_width / preview_width
            preview_width=pimage_width
            preview_height= int(preview_height*preview_ratio)

            preview=cv.resize(preview, (preview_width,preview_height))  # 프리뷰와 암호화할 사진의 가로 길이가 같아짐
            print(preview.shape, crypto_image.shape)
            crypto_image=np.vstack((preview, crypto_image))

        image_name=f"{pimage_name}_en.png"
        image_path=os.path.join(save_dir, image_name)
        cv.imwrite(image_path, crypto_image, [cv.IMWRITE_PNG_COMPRESSION,0])

        print(crypto_image[0,0,:])

        return image_name

    #복호화 함수
    def decrypt(self, save_dir, crypto_image):
        #암호화 된 이미지 불러오기(), 크기 측정
        cdata=crypto_image.read()
        pil_cimage=Image.open(BytesIO(cdata))
        cimage=np.flipud(np.array(pil_cimage.convert('RGB'))[:,:,::-1])   #encrypt()에서 프리뷰를 대비해 상하반전했으니 다시 상하반전해준다
        cimage_height, cimage_width, color=cimage.shape      # 이미지를 Mat 클래스로 가져온다. shape=(height, width, 3)이다
        cimage_name=os.path.splitext(crypto_image.name)[0]

        print(cimage[0,0,:])


        #이미지 복호화
        encrypt_data=self.aes.decrypt(cimage.tobytes())  #위 원본데이터 아래 복호화에 영향받은 프리뷰(어차피 짜를거라 상관없음)
        encrypt_image=np.frombuffer(encrypt_data, dtype=np.uint8).reshape(cimage_height, cimage_width, color)

        print(encrypt_image[0,0,:])


        #원본 높이 및 패딩 높이 찾기(암호화할 때 패딩의 제일 앞 1px(3byte)는 원본 높이, 다음 1px는 패딩 높이, 나머지는 0으로 채웠다 )
        pimage_height=encrypt_image[0,0,:]#3bytes를 단순히 더하면 안되고 2진법으로 변환후 다 이어붙여서 10진법으로 바꿔야 함
        pimage_height=int(bin(pimage_height[0])+bin(pimage_height[1])[2:]+bin(pimage_height[2])[2:],0)  #원본 이미지의 높이
        pad_height=encrypt_image[0,1,2] #패딩의 높이(1~16이라 맨 뒤에서만 뽑아도 됨)'


        #패딩, 프리뷰 제거
        plain_image=encrypt_image[pad_height:(pimage_height+pad_height),...]   # 패딩, 프리뷰(있다면)이 이과정에서 잘린다. 

        if cimage_name[-3:] == "_en" : image_name=f'{cimage_name[:-3]}.png'
        else : image_name=f"{cimage_name}_de.png"
        image_path=os.path.join(save_dir, image_name)
        cv.imwrite(image_path, plain_image)

        print(plain_image[0,0,:])

        return image_name

# 임시로 저장된 이미지를 주기적으로 삭제하는 함수
def delete_old_images(folder_path, hours=24):
    current_time = time.time()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            if current_time - creation_time > hours * 3600:
                os.remove(file_path)



        


        

        
