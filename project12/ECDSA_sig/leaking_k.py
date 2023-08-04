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

def ECDSA_leaking_k(signature, m, k):
    r, s = signature
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = (s * k - e) % N
    tmp2 = inv(r, N)
    return tmp1 * tmp2 % N


# A generate (sk, pk), compute a signature
sk, pk = ECDSA_sign_verify.key_gen()  # A publish pk for others to verify
message = "message of A"
signature, k = ECDSA_sign_and_return_k(message, sk)

# B get m, signature = (r, s) and leaking k
d = ECDSA_leaking_k(signature, message,  k)
# B forge a signature
message_for_forge = "message of B"
pk_from_d = EC_multi(d, G)
forged_signature= ECDSA_sign_verify.ECDSA_sign(message_for_forge, d)

# C get signature forged by B and verify it with pk of A
if ECDSA_sign_verify.ECDSA_verify(forged_signature, message_for_forge, pk) == 1:
    print('ECDSA sig: leaking k leads to leaking of d is successful.')