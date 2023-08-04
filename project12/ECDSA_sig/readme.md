### 代码说明

EC.py ： 椭圆曲线上某些参数的定义、一些运算：点加、点减、点乘、逆元等；

ECDSA_sv.py ： 完成了基本的ECDSA签名与验证；需要 imporyt：EC

leaking_k.py ：完成了对pitfall1：leaking k leads to leaking of d的验证；需要 import：EC、ECDSA_sv

reusing_k.py ：完成了对pitfall2：reusing k leads to leaking of d的验证；需要 import：EC、ECDSA_sv



### 运行指导

ECDSA_sv.py、leaking_k.py、reusing_k.py 已经设置好一定的消息，直接运行即可。

### 运行结果

# Project9: verify the above pitfalls with proof-of-concept code


## 202000460124 蔡欣悦

### 代码说明

EC.py ： 椭圆曲线上某些参数的定义、一些运算：点加、点减、点乘、逆元等；

ECDSA_sv.py ： 完成了基本的ECDSA签名与验证；需要 imporyt：EC

leaking_k.py ：完成了对pitfall1：leaking k leads to leaking of d的验证；需要 import：EC、ECDSA_sv

reusing_k.py ：完成了对pitfall2：reusing k leads to leaking of d的验证；需要 import：EC、ECDSA_sv

#### ECDSA签名中，对不同条件下，私钥d的推导情况、推导结果见下图：

![IMG_20220725_154507](https://user-images.githubusercontent.com/105582476/180731987-08d31063-7042-4d21-aa24-7381e1fddfbe.jpg)


### 运行指导

ECDSA_sv.py、leaking_k.py、reusing_k.py 已经设置好一定的消息，直接运行即可。

### 运行结果

- <img width="332" alt="image" src="https://user-images.githubusercontent.com/105582476/180727165-ece6389b-7691-4602-b9b7-394f1e8751a3.png">

- <img width="335" alt="image" src="https://user-images.githubusercontent.com/105582476/180727284-fbbee04d-6f56-4b61-ab6a-5ffaeaabe70f.png">


### 具体贡献

完成了对部分pitfall的证明。



### 具体贡献

完成了对部分pitfall的证明。
