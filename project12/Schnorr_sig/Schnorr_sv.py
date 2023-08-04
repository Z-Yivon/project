from EC import *
from gmssl import sm3, func
import secrets

def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = EC_multi(sk, G)  # public key
    return sk, pk

def Schnorr_sign(M, sk):
    """
    :return signature: (R, s)
    """
    k = secrets.randbelow(N)
    R = EC_multi(k, G)
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    s = k + e * sk % N
    return (R, s)


def Schnorr_verify(signature, M, pk):
    R, s = signature
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    tmp1 = EC_multi(s, G)
    tmp2 = EC_multi(e, pk)
    tmp2 = EC_add(R, tmp2)
    return tmp1 == tmp2


if __name__ == '__main__':
    sk, pk = key_gen()
    m = "Schnorr_sign_verify"
    signa = Schnorr_sign(m, sk)
    print("Success!" if Schnorr_verify(signa, m, pk) == 1 else "Fail!")