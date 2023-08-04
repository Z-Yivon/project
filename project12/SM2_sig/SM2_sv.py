import secrets
from pre_SM2 import *
from gmssl import sm3, func

A = 0
B = 7
GX = 55066263022277343669578718895168534326250603453777594175500187360389116729240
GY = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (GX, GY)
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337

def precompute(ID, a, b, GX, GY, xA, yA):
    """compute ZA = SM3(ENTL||ID||a||b||GX||GY||xA||yA)"""
    a = str(a)
    b = str(b)
    GX = str(GX)
    GY = str(GY)
    xA = str(xA)
    yA = str(yA)
    ENTL = str(get_bit_num(ID))

    joint = ENTL + ID + a + b + GX + GY + xA + yA
    joint_b = bytes(joint, encoding='utf-8')
    digest = sm3.sm3_hash(func.bytes_to_list(joint_b))
    return int(digest, 16)

def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = EC_multi(sk, G)  # public key
    return sk, pk

def sign(sk, msg, ZA):
    """SM2 signature algorithm"""
    gangM = ZA + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(gangM_b))
    e = int(e, 16)  # str -> int
    while 1:
        k = secrets.randbelow(N)  # generate random number k
        a_dot = EC_multi(k, G)  # (x1, y1) = kG
        r = (e + a_dot[0]) % N  # r = (e + x1) % n
        s = 0
        if r != 0 and r + k !=N: 
            s = (inv(1 + sk, N) * (k - r * sk)) % N
        if s != 0:  return (r, s)
    
def verify(pk, ID, msg, signature):
    """SM2 verify algorithm
    :param pk: public key
    :param ID: ID
    :param msg: massage
    :param signature: (r, s)
    :return: true/false
    """
    r = signature[0]  # r'
    s = signature[1]  # s'
    ZA = precompute(ID,A,B,G_X,G_Y,pk[0],pk[1])
    gangM = str(ZA) + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(gangM_b))  # e'
    e = int(e, 16)  # str -> int
    t = (r + s) % N

    dot1 = EC_multi(s, G)
    dot2 = EC_multi(t, pk)
    dot = EC_add(dot1, dot2)  # (x2, y2) = s'G + t'pk

    R = (e + dot[0]) % N  # R = (e' + x2) % N
    return R == r

if __name__=='__main__':
    prikey, pubkey = key_gen()
    print('pk:',pubkey)
    message = "i love you"
    ID = 'caixinyue'
    ZA = precompute(ID, A, B, GX, GY, pubkey[0], pubkey[1])
    signature = sign(prikey, message, str(ZA))
    print("sign:", signature)
    if verify(pubkey, ID, message, signature) == 1:
        print('verify:True')
