from EC import *
import secrets
from gmssl import sm3, func

def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = EC_multi(sk, G)  # public key
    return sk, pk

def ECDSA_sign(m, sk):
    """ECDSA signature algorithm
    :param m: message
    :param sk: private key
    :return signature: (r, s)
    """
    while 1:
        k = secrets.randbelow(N)  # N is prime, then k <- Zn*
        R = EC_multi(k, G)
        r = R[0] % N  # Rx mod n
        if r != 0: break
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = inv(k, N)
    tmp2 = (e + sk * r) % N
    s = tmp1 * tmp2 % N
    return (r, s)


def ECDSA_verify(signature, m, pk):
    """ECDSA algorithm
    :param signature: (r, s)
    :param m: message
    :param pk: public key
    :return:True or False
    """
    r, s = signature
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    w = inv(s, N)
    tmp1 = EC_multi(e * w, G)
    tmp2 = EC_multi(r * w, pk)
    dot = EC_add(tmp1, tmp2)
    x = dot[0]
    return x == r


if __name__ == '__main__':
    sk, pk = key_gen()
    m = "ECDSA_sign_verify"
    signa = ECDSA_sign(m, sk)
    print("Success!" if ECDSA_verify(signa, m, pk) == 1 else "Fail!")