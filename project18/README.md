# Project18: send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself

## 交易信息

打开一个比特币交易网站：https://blockchair.com/bitcoin-cash/block/804701，如下图所示：

![img](F:\创新创业实践\比特币交易\pic\1.png)

可以看到以下信息：

Hash 是这个区块的前一个区块的hash值。也就是矿工要进行计算的值。

时间戳用来标识这个区块挖出的时间

Height 指的是这个区块之前区块的数量

transaction count   这个区块内部交易的数量

Difficulty 衡量挖掘比特币区块的难度

Merkle root 指的是merkle树的根的hash值

Version 版本号

Bits 目标哈希的难度等级，表示解决 nonce 的难度

Nonce：矿工必须解决的加密数字，以验证区块。nonce 用于验证块中包含的信息，生成一个随机数，将其附加到当前标头的散列中，重新散列该值，并将其与目标散列进行比较。

Transaction Volume 比特币的交易量

reward 比特币区块奖励是奖励给 矿工的新比特币，

