### 代码说明

EC.py ： 椭圆曲线上某些参数的定义、一些运算：点加、点减、点乘、逆元等；

ECDSA_sv.py ： 完成了基本的ECDSA签名与验证；需要 imporyt：EC

leaking_k.py ：完成了对pitfall1：leaking k leads to leaking of d的验证；需要 import：EC、ECDSA_sv

reusing_k.py ：完成了对pitfall2：reusing k leads to leaking of d的验证；需要 import：EC、ECDSA_sv

# Leaking K

## 代码说明

当k的值被泄露时，攻击者可以根据公式
$$
\begin{array}{l}
s=(h+r d) k^{-1} \bmod n \\
d=(s k-h) r^{-1} \bmod n
\end{array}
$$
得到私钥值
# reusing k

## 代码描述

如果同一个人使用了两次同一个k那么私钥可以被计算得到
$$
k=\left(h_{1}-h_{2}\right)\left(s_{1}-s_{2}\right)^{-1} \bmod n
$$


### 运行指导

ECDSA_sv.py、leaking_k.py、reusing_k.py 已经设置好一定的消息，直接运行即可。

### 运行结果

- <img width="332" alt="image" src="https://user-images.githubusercontent.com/105582476/180727165-ece6389b-7691-4602-b9b7-394f1e8751a3.png">

- <img width="335" alt="image" src="https://user-images.githubusercontent.com/105582476/180727284-fbbee04d-6f56-4b61-ab6a-5ffaeaabe70f.png">



