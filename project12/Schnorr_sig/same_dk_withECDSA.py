import EC, Schnorr_sv
import secrets
from gmssl import sm3, func


def ECDSA_sign_and_return_k(m, sk):
    """ECDSA signature algorithm
    :param m: message
    :param sk: private key
    :return signature: (r, s)
    """
    while 1:
        k = secrets.randbelow(EC.N)  # N is prime, then k <- Zn*
        R = EC.EC_multi(k, EC.G)
        r = R[0] % EC.N  # Rx mod n
        if r != 0: break
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))
    e = int(e, 16)
    tmp1 = EC.inv(k, EC.N)
    tmp2 = (e + sk * r) % EC.N
    s = tmp1 * tmp2 % EC.N
    return (r, s), k

def Schnorr_sign_and_assign_k(k, M, sk):
    """
    :return signature: (R, s)
    """
    R = EC.EC_multi(k, EC.G)
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    s = k + e * sk % EC.N
    return (R, s)

def same_dk(signature1, signature2, m1, m2):
    """ECDSA->1  Schnorr->2"""
    r1, s1 = signature1
    R, s2 = signature2
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(m1, encoding='utf-8'))), 16)
    tmp = str(R[0]) + str(R[1]) + m2
    e2 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    tmp = EC.inv(s1, EC.N)
    tmp1 = (s2 - tmp * e1) % EC.N
    tmp2 = tmp * r1 + e2 % EC.N
    tmp2 = EC.inv(tmp2, EC.N)
    return tmp1 * tmp2 % EC.N

######### same d #########
sk, pk = Schnorr_sv.key_gen()

######### signature1 from ECDSA #########
message1 = "signature1 from ECSDA with sk"
signa1, k1 = ECDSA_sign_and_return_k(message1, sk)

######### signature2 from Schnorr with same d, k #########
message2 = "signature2 from ECSDA with sk, k1"
signa2 = Schnorr_sign_and_assign_k(k1, message2, sk)

######### recover d with two message #########
d = same_dk(signa1, signa2, message1, message2)



print("Success!" if d == sk else "Fail!")