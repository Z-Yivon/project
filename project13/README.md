# Project13: Implement the above ECMH scheme

## ECMH

`ECMH` 用于 hash 单个元素，`ECMH_set` 用于 hash 一个集合，把 $\mathbb{F}_{2^n}^{*}$ 上的元素映射到椭圆曲线加法群上 $G$，这样得到的 hash 就可以满足以下两条性质

* 1. $ECMH(A+B) = ECMH(A) + ECMH(B)$
* 2. $ECMH(A,B) = ECMH(B,A)$

ECMH相关代码：
```
 MultiSet Hash -> EC combine/add/remove
def add(ecmh, msg):
    dot = msg_to_dot(msg)
    tmp = EC_add(ecmh, dot)
    return tmp


def single(msg):
    return add(0, msg)


def remove(ecmh, msg):
    dot = msg_to_dot(msg)
    tmp = EC_sub(ecmh, dot)
    return tmp


def combine(msg_set):
    ans = single(msg_set[0])
    num = len(msg_set) - 1
    for i in range(num):
        ans = add(ans, msg_set[i + 1])
    return ans
```
 
## 实验环境

- python 3.10 需要安装hashlib和random库


## 实验结果

!([./ScreenShot/ECMH.png](https://github.com/Z-Yivon/project/blob/main/project13/result.png)https://github.com/Z-Yivon/project/blob/main/project13/result.png)

## 参考文献
https://eprint.iacr.org/2009/226.pdf
