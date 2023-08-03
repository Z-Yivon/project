# Project11: impl sm2 with RFC6979


## 实验环境

python 3.10 需要提前安装hashlib、hmac、sys、gmssl库


## RFC6979

参照RFC文档中的实现方式，首先可以明确大致思路如下：^[1]^

+ 设置私钥为pk，私钥长度为qlen，消息为m

1. 计算h1 = H(m),H即哈希函数，我选用的是SHA256，hlen为哈希值的比特长度
2. 设置V = 0x01 0x01... 0x01，长度为hlen
3. 设置K = 0x00 0x00... 0x00，长度为heln
4. 计算K = HMAC(V||0x00||int2octets(x)||bits2octets(h1))
5. V = HMAC(V)
6. K = HMAC(V||0x01||int2octets(x)||bits2octets(h1))
7. V = HMAC(V)
8. 执行以下循环至找到合适的K
   * 设T为空序列，T长度为tlen个bit
   * tlen<qlen时执行
     * V = HMAC(V)
     * T = T||V
   * 计算k=bits2int(T),k∈[1,q-1]，则可输出，否则计算
     * K =  HMAC(V||0x00)
     * V = HMAC(V)

按照此流程初步实现了一种写法，但是在最后的循环部分有些小瑕疵，会出bug，于是参考了pybitcointools中的处理方法，详见代码.

SM2的优势之一在于采用随机数，因此同样的明文数据每一次加密结果都不一样，而使用RFC6979生成的k值由消息与私钥决定，因此可能会得到一样的结果，故在实现中同时采用RFC6979和随机数生成k值，并将二者相加从而使每次的加密结果不同，这样既保证泄露随机数种子也不能泄密，又能使同样的明文密钥能够得到不同的加密数值。

## 代码说明

RFC6979文档中关于确定性产生k的方法如下：

```
Given the input message m, the following process is applied:

   a.  Process m through the hash function H, yielding:

          h1 = H(m)

       (h1 is a sequence of hlen bits).

   b.  Set:

          V = 0x01 0x01 0x01 ... 0x01

       such that the length of V, in bits, is equal to 8*ceil(hlen/8).
       For instance, on an octet-based system, if H is SHA-256, then V
       is set to a sequence of 32 octets of value 1.  Note that in this
       step and all subsequent steps, we use the same H function as the
       one used in step 'a' to process the input message; this choice
       will be discussed in more detail in Section 3.6.
  c.  Set:

          K = 0x00 0x00 0x00 ... 0x00

       such that the length of K, in bits, is equal to 8*ceil(hlen/8).

   d.  Set:

          K = HMAC_K(V || 0x00 || int2octets(x) || bits2octets(h1))

       where '||' denotes concatenation.  In other words, we compute
       HMAC with key K, over the concatenation of the following, in
       order: the current value of V, a sequence of eight bits of value
       0, the encoding of the (EC)DSA private key x, and the hashed
       message (possibly truncated and extended as specified by the
       bits2octets transform).  The HMAC result is the new value of K.
       Note that the private key x is in the [1, q-1] range, hence a
       proper input for int2octets, yielding rlen bits of output, i.e.,
       an integral number of octets (rlen is a multiple of 8).

   e.  Set:

          V = HMAC_K(V)

   f.  Set:

          K = HMAC_K(V || 0x01 || int2octets(x) || bits2octets(h1))

       Note that the "internal octet" is 0x01 this time.

   g.  Set:

          V = HMAC_K(V)

   h.  Apply the following algorithm until a proper value is found for
       k:

       1.  Set T to the empty sequence.  The length of T (in bits) is
           denoted tlen; thus, at that point, tlen = 0.

       2.  While tlen < qlen, do the following:

              V = HMAC_K(V)

              T = T || V
       3.  Compute:

              k = bits2int(T)

           If that value of k is within the [1,q-1] range, and is
           suitable for DSA or ECDSA (i.e., it results in an r value
           that is not 0; see Section 3.4), then the generation of k is
           finished.  The obtained value of k is used in DSA or ECDSA.
           Otherwise, compute:

              K = HMAC_K(V || 0x00)

              V = HMAC_K(V)

           and loop (try to generate a new T, and so on).

   Please note that when k is generated from T, the result of bits2int
   is compared to q, not reduced modulo q.  If the value is not between
   1 and q-1, the process loops.  Performing a simple modular reduction
   would induce biases that would be detrimental to signature security.
```

根据此文档，使用python，通过hmac，hashlib等库函数实现k的生成部分。

参考文档内容，编写生成k的函数：

```python
def deterministic_generate_k(msghash, priv):
    v = b'\x01' * 32
    k = b'\x00' * 32
    k = hmac.new(k, v+b'\x00'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v+b'\x01'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return bytes_to_int(hmac.new(k, v, hashlib.sha256).digest())
```

------

得到k后，正常的构建sm2签名体系。

使用gmssl库中的sm2相关函数实现sm2的相关功能。并进行了加解密操作，验证了加解密的一致性，以及签名的正确性。

## 运行结果

![img](https://github.com/Z-Yivon/project/blob/main/project11/result.png)





## 参考文献

[1]关于SM2国密算法开发流程[DB/OL] . (2021-04-02) https://blog.csdn.net/I_O_fly/article/details/115391340

[2]Web Encrypt-SM2加密算法[EB/OL] https://webencrypt.org/sm2/#sm2encrypt
