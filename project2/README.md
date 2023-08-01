# Project 2
## 原理
**第二原像攻击**，即给定消息M1时，攻击者能够找到另一条消息M2,其哈希值与M1的哈希值相同。理论上复杂度为$O(2^n)$  
本实验利用Pollard Rho算法实现了**第二原象攻击**，即对于指定的字符串，找到与之哈希相同的字符串。最终，在可接受的时间里，实现了$32$比特的第二原象攻击。      
Rho攻击（来自Pollard Rho算法），流程如下  
1. 给定具有n比特哈希值的哈希函数，选择一些随机哈希值H1,设H1'=H1
2. 计算H2=Hash(H1),H2'=Hash(Hash(H1'))
3. 迭代该过程并计算Hi+1=Hash(Hi)，Hi+1'=Hash(Hash(Hi'))，直到有一个i可以满足Hi+1=Hi+1'  
对应的示意图如下  
![image](https://github.com/Z-Yivon/project/blob/main/project2/headImg.png)  

## 运行环境
visual studio 2019

需要提前安装openssl库，安装方法可以参考以下网址：https://blog.csdn.net/zhizhengguan/article/details/112846817
## 运行结果
16比特运行结果截图

![image](https://github.com/Z-Yivon/project/blob/main/project2/16bit.png)

24比特运行结果截图

![image](https://github.com/Z-Yivon/project/blob/main/project2/24bit.png)
