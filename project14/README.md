# Project14: Implement a PGP scheme with SM2

## 实验环境

python 3.10 需要安装Crypto、gmssl、random等库。

## PGP简介
PGP(Pretty Good Privacy)，是一个基于RSA公钥和对称加密相结合的邮件加密软件。该系统能为电子邮件和文件存储应用过程提供认证业务和保密业务。

PGP是个混合加密算法，它由一个对称加密算法、一个非对称加密算法、与单向散列算法以及一个随机数产生器（从用户击键频率产生伪随机数序列的种子）组成。

## 实验过程
本次实验旨在实现一个简易PGP，调用GMSSL库中封装好的SM2/SM4加解密函数。

加密时使用对称加密算法SM4加密消息，非对称加密算法SM2加密会话密钥；

解密时先使用SM2解密求得会话密钥，再通过SM4和会话密钥求解原消息。

## 加密过程
![image](https://github.com/Z-Yivon/project/blob/main/project14/p2.png)

## 解密过程
![image](https://github.com/Z-Yivon/project/blob/main/project14/p1.png)

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

```
SM4 = CryptSM4()
SM4.set_key(k, SM4_ENCRYPT)
c1 = SM4.crypt_ecb(m)
```

调用GMSSL库中封装好的SM2加密函数对密钥进行加密：

```
c2 = sm2_crypt.encrypt(k)
```

返回c1与c2

## def pgp_dec(c1,c2)
PGP解密算法

调用GMSSL库中封装好的SM2解密函数对密钥进行解密：

```
k = sm2_crypt.decrypt(c2)
```

调用GMSSL库中封装好的SM4解密函数对信息进行解密：

```
SM4 = CryptSM4()
SM4.set_key(k, SM4_DECRYPT)
m = SM4.crypt_ecb(c1)
```
# 测试结果
![image](https://github.com/Z-Yivon/project/blob/main/project14/result.png)
