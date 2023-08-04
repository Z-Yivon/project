import SM2_sv, pre_SM2
import secrets
from gmssl import sm3, func


def ECDSA_sign_and_return_k(m, sk):
    """ECDSA signature algorithm
    :param m: message
    :param sk: private key
    :return signature: (r, s)
    """
    while 1:
        k = secrets.randbelow(pre_SM2.N)  # N is prime, then k <- Zn*
        R = pre_SM2.EC_multi(k, pre_SM2.G)
        r = R[0] % pre_SM2.N  # Rx mod n
        if r != 0: break
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = pre_SM2.inv(k, pre_SM2.N)
    tmp2 = (e + sk * r) % pre_SM2.N
    s = tmp1 * tmp2 % pre_SM2.N
    return (r, s), k

def sign_and_assign_k(k, sk, msg, ZA):
    """SM2 signature algorithm"""
    gangM = ZA + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(gangM_b))
    e = int(e, 16)  # str -> int
    a_dot = pre_SM2.EC_multi(k, pre_SM2.G)  # (x1, y1) = kG
    r = (e + a_dot[0]) % pre_SM2.N  # r = (e + x1) % n
    s = 0
    if r != 0 and r + k != pre_SM2.N: 
        s = (pre_SM2.inv(1 + sk, pre_SM2.N) * (k - r * sk)) % pre_SM2.N
    if s != 0:  return (r, s), k

def same_dk(signature1, signature2, m1):
    """ECDSA->1  SM2->2"""
    r1, s1 = signature1
    r2, s2 = signature2
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(m1, encoding='utf-8'))) , 16)
    tmp1 = s1 * s2 - e1 % pre_SM2.N
    tmp2 = r1 - s1 * s2 - s1 * r2 % pre_SM2.N
    tmp2 = pre_SM2.inv(tmp2, pre_SM2.N)
    return tmp1 * tmp2 % pre_SM2.N


######### same d #########
sk, pk = SM2_sv.key_gen()

######### signature1 from ECDSA #########
message1 = "signature1 from ECSDA with sk"
signa1, k1 = ECDSA_sign_and_return_k(message1, sk)

######### signature2 from SM2 with same d, k #########
message2 = "signature2 from ECSDA with sk, k1"
ID = 'SM2_same_dk_with_ECDSA'
ZA = SM2_sv.precompute(ID, SM2_sv.A, SM2_sv.B, SM2_sv.GX, SM2_sv.GY, pk[0], pk[1])
signa2, k2 = sign_and_assign_k(k1, sk, message2, str(ZA))

######### recover d with two message #########
d = same_dk(signa1, signa2, message1)



print("Success!" if d == sk else "Fail!")