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

def Schnorr_reusing_k(signature1, signature2, m1, m2):
    R1, s1 = signature1
    R2, s2 = signature2
    if R1 != R2: return 'error'
    R = R1
    tmp = str(R[0]) + str(R[1]) + m1
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    tmp = str(R[0]) + str(R[1]) + m2
    e2 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))) , 16)
    tmp1 = (s1 - s2) % N
    tmp2 = (e1 - e2) % N
    tmp2 = inv(tmp2, N)
    return tmp1 * tmp2 % N

######### A generate (sk, pk), compute a signature #########
sk, pk = Schnorr_sv.key_gen()  # A publish pk for others to verify
message1 = "message1 of A"
message2 = "message2 of A"
k = secrets.randbelow(N)  # the random number for sig
signature1 = Schnorr_sign_and_assign_k(k, message1, sk)
signature2 = Schnorr_sign_and_assign_k(k, message2, sk)

######### B get m1, m2, signature1, signature2 #########
d = Schnorr_reusing_k(signature1, signature2, message1, message2)
######### B forge a signature #########
message_for_forge = "message of B"
pk_from_d = EC_multi(d, G)
forged_signature= Schnorr_sv.Schnorr_sign(message_for_forge, d)

######### C get signature forged by B and verify it with pk of A #########
if Schnorr_sv.Schnorr_verify(forged_signature, message_for_forge, pk) == 1:
    print('ECDSA sig: reusing k leads to leaking of d is successful.')