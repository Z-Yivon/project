from hashlib import sha256
from random import randint

def SHA256(s):
    """string -> hexdigest"""
    msg = bytes(bytearray(s, encoding='utf-8'))
    return sha256(msg).hexdigest()


def inv(a, n):
    '''求逆'''

    def ext_gcd(a, b, arr):
        '''扩欧'''
        if b == 0:
            arr[0] = 1
            arr[1] = 0
            return a
        g = ext_gcd(b, a % b, arr)
        t = arr[0]
        arr[0] = arr[1]
        arr[1] = t - int(a / b) * arr[1]
        return g

    arr = [0, 1, ]
    gcd = ext_gcd(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1


def ECC_add(p, q):
    """椭圆曲线加法"""
    # 0 means inf
    if p == 0 and q == 0:
        return 0  # 0 + 0 = 0
    elif p == 0:
        return q  # 0 + q = q
    elif q == 0:
        return p  # p + 0 = p
    else:
        if p[0] == q[0]:
            if (p[1] + q[1]) % P == 0:
                return 0  # mutually inverse
            elif p[1] == q[1]:
                return ECC_double(p)
        elif p[0] > q[0]:  # swap if px > qx
            tmp = p
            p = q
            q = tmp
        r = []
        slope = (q[1] - p[1]) * inv(q[0] - p[0], P) % P  # 斜率
        r.append((slope ** 2 - p[0] - q[0]) % P)
        r.append((slope * (p[0] - r[0]) - p[1]) % P)
        return (r[0], r[1])


def ECC_inv(p):
    """椭圆曲线逆元"""
    r = [p[0]]
    r.append(P - p[1])
    return r


def ECC_sub(p, q):
    """椭圆曲线减法：p - q"""
    q_inv = ECC_inv(q)
    return ECC_add(p, q_inv)


def ECC_double(p):
    """椭圆曲线双倍点运算"""
    r = []
    slope = (3 * p[0] ** 2 + A) * inv(2 * p[1], P) % P
    r.append((slope ** 2 - 2 * p[0]) % P)
    r.append((slope * (p[0] - r[0]) - p[1]) % P)
    return (r[0], r[1])


def ECC_mult(s, p):
    """椭圆曲线多倍点运算
    :param s: 倍数
    :param p: 点
    :return: 运算结果
    """
    n = p
    r = 0
    s_bin = bin(s)[2:]
    s_len = len(s_bin)

    for i in reversed(range(s_len)):  # 类快速幂思想
        if s_bin[i] == '1':
            r = ECC_add(r, n)
        n = ECC_double(n)

    return r


def msg_to_dot(msg):
    x = int(SHA256(msg), 16) % N
    dot = ECC_mult(x, G)
    return dot


# MultiSet Hash -> EC combine/add/remove
def add(ecmh, msg):
    dot = msg_to_dot(msg)
    tmp = ECC_add(ecmh, dot)
    return tmp


def single(msg):
    return add(0, msg)


def remove(ecmh, msg):
    dot = msg_to_dot(msg)
    tmp = ECC_sub(ecmh, dot)
    return tmp


def combine(msg_set):
    ans = single(msg_set[0])
    num = len(msg_set) - 1
    for i in range(num):
        ans = add(ans, msg_set[i + 1])
    return ans

#参数设置
A = 0
B = 7
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337

#验证部分
m1 = "zyf"
m2 = "202100460108"
m3 = "wang_an"
m11 = [m1, m1]
m12 = [m1, m2]
m13 = [m1, m3]
m21 = [m2, m1]
m123 = [m1, m2, m3]
m132 = [m1, m3, m2]
m231 = [m2, m3, m1]
m321 = [m3, m2, m1]

print('========= duplicate elements=========')
print('ECMH(m1):\n', single(m1))
print('ECMH(m1 + m1):\n', combine(m11))
print('ECMH(m1) + ECMH(m1):\n', add(single(m1), m1))

print('\n========= add =========')
print('ECMH(m1):\n', single(m1))
print('ECMH(m2):\n', single(m2))
print('ECMH(m1 + m2):\n', combine(m12))
print('ECMH(m1) + ECMH(m2):\n', add(single(m1), m2))

print('\n========= remove =========')
print('ECMH(m1) + ECMH(m2) + ECMH(m3):\n',add(add(single(m1), m2),m3))
print('ECMH(m1 + m2 + m3):\n', combine(m123))
print('ECMH(m1 + m2):\n', combine(m12))
print('ECMH(m1 + m2 + m3) - ECMH(m3):\n', remove(combine(m123), m3))

print('\n========= order does not matter =========')
print('ECMH(m1 + m2 + m3):\n', combine(m123))
print('ECMH(m2 + m3 + m1):\n', combine(m231))
print('ECMH(m3 + m2 + m1):\n', combine(m321))







