#先于client.py运行
import  ECC
import random
import hashlib
import socket
import json

def init():
    n=ECC.get_n()
    return (n,ECC.get_G(),random.randrange(1, n),random.randrange(1, n),random.randrange(1, n))
#n,G,d2,k2,k3
def Gen_pk(d2,P1,G,n):
    id2=ECC.multi_inverse(d2,n)
    G_ne=ECC.Neg_ele(G)
    pk=ECC.Point_Add(ECC.Multi(id2,P1),G_ne)
    print("public key:", pk)
    return pk
def Gen_r(d2,k2,k3,Q1,e,n,G):
    Q2=ECC.Multi(k2,G)
    x1,y1=ECC.Point_Add(ECC.Multi(k3,Q1),Q2)
    r=(x1+e)%n
    s2=(d2*k3)%n
    s3=(d2*(r+k2))%n
    return (r,s2,s3)


#msg=input("请输入Z,M\n")
#Z,M=msg.split(" ")
HOST="127.0.0.1"
PORT=5088
dst=("127.0.0.1",9000)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定端口和端口号
s.bind((HOST,PORT))
print("当前监听地址：",(HOST,PORT))

n,G,d2,k2,k3=init()
print("————————————————————————————初始化成功————————————————————————————")
print("n=",n,"\nG=",G,"\nd2=",d2,"\nk2=",k2,"\nk3=",k3)

temp=s.recv(1024)
P1=json.loads(temp.decode("utf-8"))
pk=Gen_pk(d2,P1,G,n)
print("-"*20+"Public Key 生成成功"+"-"*20)
print("pk ",pk)

s.sendto(json.dumps(pk).encode("utf-8"),dst)
Q1e=s.recv(1024)
Q1,e=json.loads(Q1e.decode("utf-8"))
s.sendto(json.dumps(Gen_r(d2,k2,k3,Q1,e,n,G)).encode("utf-8"),dst)


