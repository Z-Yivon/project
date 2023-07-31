#include <stdio.h>
#include <string.h>
#include<openssl/evp.h>
#include<string.h>
#include<time.h>


/**
 * @brief 计算一段数据的哈希值（原始、截断）
 *
 * @param str 数据
 * @param len 数据长度
 * @param hash_result 哈希值
 * @return unsigned int 原始哈希值长度
 */
unsigned int SM3_hash(unsigned char* str, const size_t len, unsigned char* hash_result)
{
    unsigned int ret;
    const EVP_MD* alg = EVP_sm3();
    EVP_Digest(str, len, hash_result, &ret, alg, NULL);
    return ret;
}


/**
 * @brief 生成随机字符串
 * @param length 产生字符串的长度
 * @return char* 随机字符串
 */
unsigned char* strRand(int length)
{
    int tmp;							// tmp: 暂存一个随机数
    unsigned char* buffer;						// buffer: 保存返回值
    buffer = (unsigned char*)malloc(sizeof(unsigned char) * length);

    srand((unsigned)time(NULL));
    for (int i = 0; i < length; i++) {
        tmp = rand() % 62;	        // 随机一个小于 62 的整数，0-9、a-z、A-Z 共 62 种字符
        if (tmp < 10) {			// 如果随机数小于 10，变换成一个阿拉伯数字的 ASCII
            tmp += '0';
        }
        else if (tmp < 36) {
            tmp -= 10;
            tmp += 'a';
        }
        else {				// 否则，变换成一个大写字母的 ASCII
            tmp -= 36;
            tmp += 'A';
        }
        buffer[i] = tmp;
    }
    return buffer;
}


int main(int argc, char const* argv[])
{
    int HASH_RESULT_LEN = 32;  //原始hash长度 32*8=256bits
    int HASH_ATTCK_LEN = 2;   // 截断后的长度为3x8bits（原hash结果的前4位）
    srand((unsigned)time(NULL));
    const int length = 15;
    unsigned char* data = strRand(length); //生成随机字符串

    unsigned char H1[32]; 
    SM3_hash(data, strlen((char*)data), H1);      // H1 = Hash(data)

    unsigned char H1_[32]="";   //记录碰撞的hash
    clock_t start = clock();
    unsigned char a[32];     // 记录产生碰撞的字符串
    unsigned char b[32];
    unsigned char *ss;
    while (memcmp(H1, H1_, HASH_ATTCK_LEN))    // 找到碰撞，终止循环
    {
        ss = strRand(length);
        memcpy(H1_, ss, length);
        memcpy(a, H1, HASH_RESULT_LEN);
        memcpy(b, H1_, HASH_RESULT_LEN);
        SM3_hash(H1_, HASH_RESULT_LEN , H1_);
    }
    clock_t end = clock();

    printf("Find the collision!(%d bits)\n", HASH_ATTCK_LEN * 8);

    /*      print collision      */

    printf("Initial string:%s\n", data);
    printf("data(in hex) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", a[i]);
    }
    printf("\n");

    printf("find_data(in hex) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", b[i]);
    }

    printf("\nH1  = ");

    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", H1[i]);
    }
    printf("\n");

    printf("H1_  = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", H1_[i]);
    }

    printf("\nRunning time = %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}