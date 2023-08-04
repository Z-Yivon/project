# Project19: forge a signature to pretend that you are Satoshi

## 代码说明

该项目实现了应用在比特币中的ECDSA签名在不检查消息明文m的情况下合法签名的伪造。

首先实现ECDSA签名及其验证过程。

![image-20220730170420020](./algorithm.png)

由于项目场景的需求，验签算法不检查消息明文m而是直接使用其hash值e。具体流程见上图：