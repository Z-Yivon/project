#Project13: Implement the above ECMH scheme

file: ECMH.py

Project: Implement the above ECMH scheme

参考文献：https://eprint.iacr.org/2009/226.pdf

根据上述参考文献，实现了其中最朴素的 ‘Try-and-Increment’ Method，算法如下：

![pic](./ScreenShot/TImethod.png)

`ECMH` 用于 hash 单个元素，`ECMH_set` 用于 hash 一个集合，把 $\mathbb{F}_{2^n}^{*}$ 上的元素映射到椭圆曲线加法群上 $G$，这样得到的 hash 就可以满足以下两条性质

* 1. $ECMH(A+B) = ECMH(A) + ECMH(B)$
* 2. $ECMH(A,B) = ECMH(B,A)$

```
def ECMH(u):
    h = int(hashlib.sha256(str(u).encode()).hexdigest(), 16)
    i = 0
    while(1):
        x = h + i
        d = (x ** 3 + a * x + b) % p
        if pow(d, (p - 1) // 2, p) % p == 1:
            y = modular_sqrt(d, p)
            return [x, y]

def ECMH_set(s):
    s = set(s)
    result = [0, 0]
    for x in s:
        result[0] += ECMH(x)[0]
        result[1] += ECMH(x)[1]
    return result
```
 
## 代码说明

- 代码包含SM2系统参数，以及椭圆曲线上的一些运算：点加、点减、逆元、点乘等；

- 对于消息，先利用sha256算法进行哈希，并尝试将该hash值映射到椭圆曲线上的某点；我原本尝试以哈希值为横坐标，求解纵坐标，但在循环群上求解开方较困难：我尝试了穷举以及Cipolla算法，都难以得到结果；

## 实验结果：

![pic](./ScreenShot/ECMH.png)
