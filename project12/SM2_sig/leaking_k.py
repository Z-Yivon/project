import pre_SM2, SM2_sv
from gmssl import sm3, func
import secrets

def sign_and_return_k(sk, msg, ZA):
    """SM2 signature algorithm for leaking k"""
    gangM = ZA + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(gangM_b))
    e = int(e, 16)  # str -> int
    while 1:
        k = secrets.randbelow(pre_SM2.N)  # generate random number k
        a_dot = pre_SM2.EC_multi(k, pre_SM2.G)  # (x1, y1) = kG
        r = (e + a_dot[0]) % pre_SM2.N  # r = (e + x1) % n
        s = 0
        if r != 0 and r + k != pre_SM2.N: 
            s = (pre_SM2.inv(1 + sk, pre_SM2.N) * (k - r * sk)) % pre_SM2.N
        if s != 0:  return (r, s), k

def SM2_leaking_k(signature, k):
    """SM2 signature: leaking k leads to leaking of d
    :param signature: (r, s)
    :param k: leaking k
    :return d: private key of SM2 signature
    """
    r, s = signature
    tmp1 =  pre_SM2.inv((s + r), pre_SM2.N)
    tmp2 = (k - s) % pre_SM2.N
    d = tmp1 * tmp2 % pre_SM2.N
    return  d



######### A generate (sk, pk), compute a signature #########
sk, pk = SM2_sv.key_gen()  # A publish pk for others to verify
message = "test: SM2 leaking k"
ID = 'SM2_leaking_k_userA'
ZA = SM2_sv.precompute(ID, SM2_sv.A, SM2_sv.B, SM2_sv.GX, SM2_sv.GY, pk[0], pk[1])
signature, k = sign_and_return_k(sk, message, str(ZA))

######### B get signature = (r, s) and leaking k #########
d = SM2_leaking_k(signature, k)

######### B forge a signature #########
message_for_forge = "test: SM2 leaking k: B forge a signature"
ID_for_forge = ID
pk_from_d = pre_SM2.EC_multi(d, pre_SM2.G)
ZA_for_forge = SM2_sv.precompute(ID_for_forge, SM2_sv.A, SM2_sv.B, SM2_sv.GX, SM2_sv.GY, pk_from_d[0], pk_from_d[1])
forged_signature= SM2_sv.sign(d, message_for_forge, str(ZA_for_forge))

######### C get signature forged by B and verify it with pk&ID of A #########
if SM2_sv.verify(pk, ID, message_for_forge, forged_signature) == 1:
    print('SM2 sig: leaking k leads to leaking of d is successful.')