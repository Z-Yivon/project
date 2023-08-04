from EC import *
from gmssl import sm3, func
import secrets
import Schnorr_sv

def Schnorr_sign_and_assign_k(k, M, sk):
    """
    :return signature: (R, s)
    """
    R = EC_multi(k, G)
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    s = k + e * sk % N
    return (R, s)

def Schnorr_leaking_k(signature, m, k):
    R, s = signature
    tmp = str(R[0]) + str(R[1]) + m
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    tmp1 = s - k % N
    tmp2 = inv(e, N)
    return tmp1 * tmp2 % N

######### A generate (sk, pk), compute a signature #########
sk, pk = Schnorr_sv.key_gen()  # A publish pk for others to verify
message = "message of A"
k = secrets.randbelow(N)  # the random number for sig
signature = Schnorr_sign_and_assign_k(k, message, sk)

######### B get m, signature = (R, s) and leaking k #########
d = Schnorr_leaking_k(signature, message,  k)
######### B forge a signature #########
message_for_forge = "message of B"
pk_from_d = EC_multi(d, G)
forged_signature= Schnorr_sv.Schnorr_sign(message_for_forge, d)

######### C get signature forged by B and verify it with pk of A #########
if Schnorr_sv.Schnorr_verify(forged_signature, message_for_forge, pk) == 1:
    print('ECDSA sig: leaking k leads to leaking of d is successful.')