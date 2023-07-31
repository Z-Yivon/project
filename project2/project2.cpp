#include <stdio.h>
#include <string.h>
#include<openssl/evp.h>
#include<string.h>
#include<time.h>


/**
 * @brief ����һ�����ݵĹ�ϣֵ��ԭʼ���ضϣ�
 *
 * @param str ����
 * @param len ���ݳ���
 * @param hash_result ��ϣֵ
 * @return unsigned int ԭʼ��ϣֵ����
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
 * @brief ��������ַ���
 * @param length �����ַ����ĳ���
 * @return char* ����ַ���
 */
unsigned char* strRand(int length)
{
    int tmp;							// tmp: �ݴ�һ�������
    unsigned char* buffer;						// buffer: ���淵��ֵ
    buffer = (unsigned char*)malloc(sizeof(unsigned char) * length);

    srand((unsigned)time(NULL));
    for (int i = 0; i < length; i++) {
        tmp = rand() % 62;	        // ���һ��С�� 62 ��������0-9��a-z��A-Z �� 62 ���ַ�
        if (tmp < 10) {			// ��������С�� 10���任��һ�����������ֵ� ASCII
            tmp += '0';
        }
        else if (tmp < 36) {
            tmp -= 10;
            tmp += 'a';
        }
        else {				// ���򣬱任��һ����д��ĸ�� ASCII
            tmp -= 36;
            tmp += 'A';
        }
        buffer[i] = tmp;
    }
    return buffer;
}


int main(int argc, char const* argv[])
{
    int HASH_RESULT_LEN = 32;  //ԭʼhash���� 32*8=256bits
    int HASH_ATTCK_LEN = 3;   // �ضϺ�ĳ���Ϊ3x8bits��ԭhash�����ǰ4λ��
    srand((unsigned)time(NULL));
    int length = rand() % 100;
    unsigned char* sr = strRand(length);        // ��������ַ���sr
/**
 * ���Ŷ���
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
    unsigned char a[32];     // ��¼������ײ���ַ���
    unsigned char b[32];
    while (memcmp(H1, H1_, HASH_ATTCK_LEN))    // �ҵ���ײ����ֹѭ��
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