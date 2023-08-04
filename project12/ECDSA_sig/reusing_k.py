from EC import *
import secrets
import ECDSA_sign_verify
from gmssl import sm3, func

def ECDSA_sign_and_return_k(m, sk):
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
    return (r, s), k

def ECDSA_sign_and_assign_k(m, k, sk):
    """ECDSA signature algorithm
    :param m: message
    :param sk: private key
    :return signature: (r, s)
    """
    R = EC_multi(k, G)
    r = R[0] % N  # Rx mod n
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = inv(k, N)
    tmp2 = (e + sk * r) % N
    s = tmp1 * tmp2 % N
    return (r, s), k

def ECDSA_reusing_k(m1, m2, signature1, signature2):
    r, s1 = signature1
    r2, s2 = signature2
    e1 = sm3.sm3_hash(func.bytes_to_list(bytes(m1, encoding='utf-8')))  # e = hash(m)
    e1 = int(e1, 16)
    e2 = sm3.sm3_hash(func.bytes_to_list(bytes(m2, encoding='utf-8')))  # e = hash(m)
    e2 = int(e2, 16)
    tmp1 = (e1 - e2) % N
    tmp1 = tmp1 * s2 % N
    tmp2 = (s1 - s2) % N
    tmp2 = inv(tmp2, N)
    tmp1 = tmp1 * tmp2 -e2 % N
    tmp2 = inv(r, N)
    return  tmp1 * tmp2 % N


######### A generate (sk, pk), compute two signatures #########
sk, pk = ECDSA_sign_verify.key_gen()  # A publish pk for others to verify
message1 = "message1 of A"
message2 = "message2 of A"
signature1, k1 = ECDSA_sign_and_return_k(message1, sk)
signature2, k2 = ECDSA_sign_and_assign_k(message2, k1, sk)
print("reuse k" if k1 == k2 else "error")

######### B get m1, m2, signature1, signature2#########
d = ECDSA_reusing_k(message1, message2, signature1, signature2)
######### B forge a signature #########
message_for_forge = "message of B"
pk_from_d = EC_multi(d, G)
forged_signature= ECDSA_sign_verify.ECDSA_sign(message_for_forge, d)

######### C get signature forged by B and verify it with pk of A #########
if ECDSA_sign_verify.ECDSA_verify(forged_signature, message_for_forge, pk) == 1:
    print('ECDSA sig: reusing k leads to leaking of d is successful.')
else: print("Failed.")
