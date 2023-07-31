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

unsigned int SM3_hash_hash(unsigned char* str, const size_t len, unsigned char* hash_result)
{
    unsigned int ret1, ret2;
    const EVP_MD* alg = EVP_sm3();
    unsigned char middle[32];
    EVP_Digest(str, len, (unsigned char*)middle, &ret1, alg, NULL);
    EVP_Digest(middle, ret1, hash_result, &ret2, alg, NULL);
    return ret2;
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
    int HASH_ATTCK_LEN = 3;   // 截断后的长度为3x8bits（原hash结果的前4位）
    srand((unsigned)time(NULL));
    int length = rand() % 100;
    unsigned char* sr = strRand(length);        // 生成随机字符串sr
/**
 * 符号定义
 * H1 = Hash(sr), H1_ = H1
 * H1 = hash(H1), H1_ = hash(hash(H1_))
 */
    unsigned char H1[32];
    SM3_hash(sr, strlen((char*)sr), H1);      // H1 = Hash(sr)
    unsigned char H1_[32];
    memcpy(H1_, (char*)H1, HASH_RESULT_LEN);     // H1_ = H1


    SM3_hash(H1, HASH_RESULT_LEN, H1);     // H1 = hash(H1)
    SM3_hash_hash(H1_, HASH_RESULT_LEN, H1_);     // H1_ = hash(hash(H1_))

    clock_t start = clock();
    unsigned char a[32];     // 记录产生碰撞的字符串
    unsigned char b[32];
    while (memcmp(H1, H1_, HASH_ATTCK_LEN))    // 找到碰撞，终止循环
    {
        memcpy(a, H1, HASH_RESULT_LEN);
        memcpy(b, (char*)H1_, HASH_RESULT_LEN);
        SM3_hash(H1, HASH_RESULT_LEN, H1);     // H1 = hash(H1)
        SM3_hash_hash(H1_, HASH_RESULT_LEN, H1_);     // H1_ = hash(hash(H1_))
    }
    clock_t end = clock();

    printf("Find the collision!(%d bits)\n", HASH_ATTCK_LEN * 8);

    /*      print collision      */

    printf("Initial string:%s\n", sr);
    printf("a(in hex) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", a[i]);
    }
    printf("\n");

    printf("b(in hex) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", b[i]);
    }
    printf("\nhash(b)(in hex) = ");

    SM3_hash(b, HASH_RESULT_LEN, b);
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", b[i]);
    }
    printf("\nH1 = hash(a) = ");

    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", H1[i]);
    }
    printf("\n");

    printf("H1_ = hash(hash(b)) = ");
    for (int i = 0; i < HASH_RESULT_LEN; i++) {
        printf("%02x", H1_[i]);
    }

    printf("\nRunning time = %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}