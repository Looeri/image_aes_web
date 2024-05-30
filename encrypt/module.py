from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import numpy as np

#numpy를 사용해서 암/복호화 속도를 높일 것

class ImageAES():
    def __init__(self, key=None):
        self.iv=b'Z%$\xec\xe1Y\x894\x88\xa8\xb7\x08\xd0\xdb\xb2\r' #16byte의 iv(초기화 벡터)
        
        if key==None : key="this is key."  #사용자가 암호 입력하지 않으면 사용하는 암호. 암호를 감추기 위해 위에 바로 안적음.
        self.key=SHA256.new(key.encode('utf-8')).digest()

        self.aes=AES.new(self.key, AES.MODE_CBC, self.iv)
        
    def encrypt(self, imageblock):
        try:
            return self.aes.encrypt(imageblock)
        except : ValueError
            
        

    def decrypt(self, imageblock):
        try:
            return self.aes.decrypt(imageblock)
        except : ValueError


        












#AES-256 사용을 위해 32byte짜리 키를 만듬(sha256을 이용해 해시로 만듬)
def key_256(key=None):
    if key == None :  #유저가 입력한 키가 없으면 사이트에서 지정한 키 사용(tmp key의 해시)
        key="tmp key"

    k=SHA256.new()
    k.update(key)

    return k.digest()


def IV() :
    iv=b'\x8dH\xfd\xce\xd5\xae/\xcf\x0c1~\x1a\xd7\x0bh\x85' #16byte 짜리의 iv(초기화 벡터)

    return iv


