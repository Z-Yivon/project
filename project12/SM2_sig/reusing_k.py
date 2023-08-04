import pre_SM2, SM2_sv
from gmssl import sm3, func
import secrets

def sign_and_return_k(sk, msg, ZA):
    """SM2 signature algorithm"""
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

def SM2_reusing_k(signature1, signature2):
    """d = (s2 - s1)/(s1 - s2 + r1 - r2) mod N"""
    r1, s1 = signature1
    r2, s2 = signature2
    tmp1 = (s2 - s1) % pre_SM2.N
    tmp2 = (s1 - s2 + r1 - r2) % pre_SM2.N
    tmp2 = pre_SM2.inv(tmp2, pre_SM2.N)
    return tmp1 * tmp2 % pre_SM2.N


######### A generate (sk, pk), compute two signatures #########
sk, pk = SM2_sv.key_gen()  # A publish pk for others to verify
message1 = "test: SM2 reusing k_1"
message2 = "test: SM2 reusing k_2"
ID = 'SM2_reusing_k_userA'
ZA = SM2_sv.precompute(ID, SM2_sv.A, SM2_sv.B, SM2_sv.GX, SM2_sv.GY, pk[0], pk[1])
signature1, k1 = sign_and_return_k(sk, message1, str(ZA))  # return k
signature2, k2 = sign_and_assign_k(k1, sk, message2, str(ZA))  # reuse k
print("reuse k" if k1 == k2 else "error")

######### B get signature1 and signature2 #########
d = SM2_reusing_k(signature1, signature2)

######### B forge a signature #########
message_for_forge = "test: SM2 reusing k: B forge a signature"
ID_for_forge = ID
pk_from_d = pre_SM2.EC_multi(d, pre_SM2.G)
ZA_for_forge = SM2_sv.precompute(ID_for_forge, SM2_sv.A, SM2_sv.B, SM2_sv.GX, SM2_sv.GY, pk_from_d[0], pk_from_d[1])
forged_signature= SM2_sv.sign(d, message_for_forge, str(ZA_for_forge))
######### C get signature forged by B and verify it with pk&ID of A #########
if SM2_sv.verify(pk, ID, message_for_forge, forged_signature) == 1:
    print('SM2 sig: leaking k leads to reusing of d is successful.')