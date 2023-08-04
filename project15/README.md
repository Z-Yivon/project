# Project15: implement sm2 2P sign with real network communication




该项目使用 python 的 socket 网络编程模拟实际网络，实现了下图的 SM2 签名流程，使用的曲线如下。
=======
## 实验环境

python 3.10

先运行server.py文件，再运行client.py文件。
## PGP简介
PGP(Pretty Good Privacy)，是一个基于RSA公钥和对称加密相结合的邮件加密软件。该系统能为电子邮件和文件存储应用过程提供认证业务和保密业务。

PGP是个混合加密算法，它由一个对称加密算法、一个非对称加密算法、与单向散列算法以及一个随机数产生器（从用户击键频率产生伪随机数序列的种子）组成。

## 实验过程
本次实验旨在实现一个简易PGP，调用GMSSL库中封装好的SM2/SM4加解密函数。

加密时使用对称加密算法SM4加密消息，非对称加密算法SM2加密会话密钥；

解密时先使用SM2解密求得会话密钥，再通过SM4和会话密钥求解原消息。

## 加密过程
![image](https://user-images.githubusercontent.com/105578152/180976048-bc82649d-e801-4a28-a5c2-3a340b11e63f.png)

## 解密过程
![image](https://user-images.githubusercontent.com/105578152/180976114-0d3a1d28-5c1b-4034-ad68-6da4d6779308.png)

# 部分代码说明
## def epoint_mod(a, n)
定义椭圆曲线上的模运算，返回值等于a mod n

## def epoint_modmult(a, b, n)
定义椭圆曲线上的模乘运算，返回值等于a*b^(-1) mod n

## def epoint_add(P, Q, a, p)
定义椭圆曲线上的加法运算，返回值等于P + Q

## def epoint_mult(k, P, a, p)
定义椭圆曲线上的点乘运算，返回值等于k * P

## def keygen(a, p, n, G)
生成SM2算法的公私钥对

## def pgp_enc(m,k)
PGP加密算法

加密之前要先对消息进行填充，SM4分组长度为128比特即16个字节，填充完成后，需要将消息m与密钥k转化为bytes类型。

调用GMSSL库中封装好的SM4加密函数对信息进行加密：
>>>>>>> 8d7f019ed7ab9c4adf257e361f4e3114c21846e3

```
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
G = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7, 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
```


结果如图，实现双方交互，并成功签名：

![pic](https://github.com/Z-Yivon/project/blob/main/project15/result.png)
