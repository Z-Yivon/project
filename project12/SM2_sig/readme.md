

### 代码说明

pre_SM2.py ： 椭圆曲线上某些参数的定义、一些运算：点加、点减、点乘、逆元等；

SM2_sv.py ： 完成了基本的ECDSA签名与验证；需要 imporyt：pre_SM2

leaking_k.py ：完成了对pitfall1：leaking k leads to leaking of d的验证；需要 import：pre_SM2、SM2_sv

reusing_k.py ：完成了对pitfall2：reusing k leads to leaking of d的验证；需要 import：pre_SM2、SM2_sv

same_dk_withECDSA.py ：完成了对pitfall7：same d and k with ECDSA, leads to leaking of d的验证；需要 import：pre_SM2、SM2_sv


### 运行指导

ECDSA_sv.py、leaking_k.py、reusing_k.py、same_dk_withECDSA.py 已经设置好一定的消息，直接运行即可。



