import copy
import hashlib

def gcd(a, b):
    k = a // b
    remainder = a % b
    while remainder != 0:
        a = b
        b = remainder
        k = a // b
        remainder = a % b
    return b


# 改进欧几里得算法求线性方程的x与y
def euclid(a, b):
    if b == 0:
        return 1, 0
    else:
        k = a // b
        remainder = a % b
        x1, y1 = euclid(b, remainder)
        x, y = y1, x1 - k * y1
    return x, y


# 返回乘法逆元
def inverse(a, b):
    # 将初始b的绝对值进行保存
    if b < 0:
        m = abs(b)
    else:
        m = b

    flag = gcd(a, b)
    # 判断最大公约数是否为1，若不是则没有逆元
    if flag == 1:
        x, y = euclid(a, b)
        x0 = x % m  # 对于Python '%'就是求模运算，因此不需要'+m'
        # print(x0) #x0就是所求的逆元
        return x0

    else:
        print("Do not have!")

### y^2=x^3+ax+by mod (mod_value)
def Point_Add(P,Q):
    if P[0] == Q[0]:
        fenzi = (3 * pow(P[0], 2) + a)
        fenmu = (2 * P[1])
        if fenzi % fenmu != 0:
            val = inverse(fenmu, 17)
            y = (fenzi * val) % 17
        else:
            y = (fenzi / fenmu) % 17
    else:
        fenzi = (Q[1] - P[1])
        fenmu = (Q[0] - P[0])
        if fenzi % fenmu != 0:
            val = inverse(fenmu, 17)
            y = (fenzi * val) % 17
        else:
            y = (fenzi / fenmu) % 17

    Rx = (pow(y, 2) - P[0] - Q[0]) % 17
    Ry = (y * (P[0] - Rx) - P[1]) % 17
    return(Rx,Ry)


def Multi(n, point):
    if n == 0:
         return 0
    elif n == 1:
        return point

    t = point
    while (n >= 2):
        t = Point_Add(t, point)
        n = n - 1
    return t


def double(point):
    return Point_Add(point,point)


def fast_Multi(n, point):
    if n == 0:
         return 0
    elif n == 1:
        return point
    elif n%2==0:
        return Multi(n/2,double(point))
    else:
        return Point_Add(Multi((n-1)/2,double(point)),point)


def sign(m, G, d,k):
    e = Hash(m)
    R = Multi(k, G)   #R=kg
    #print("R",R)
    r = R[0] % mod_value      #r=R[x] mod mod_value
    s = (inverse(k, mod_value) * (e + d * r)) % mod_value
    return r, s

def verify(m, G, r, s, P):
    hash_m = Hash(m)
    inverse_s = inverse(s, mod_value)
    value1 = (hash_m * inverse_s) % mod_value
    value2 = (r * inverse_s) % mod_value
    w = Point_Add(Multi(value1, G), Multi(value2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % mod_value == r):
            print("签名验证通过")
            return True
        else:
            print('签名不通过')
            return False

def Hash(string):
    hash = hashlib.sha256()
    hash.update(string.encode())
    res = hash.hexdigest()
    return int(res,16)


def deduce_pubkey(s, r, k, G):
    inverse_value=inverse((s+r),17)

    k_value=Multi(k,G)

    s_value=Multi(s,G)
    value=(s_value[0],(-s_value[1])%17)
    print(k_value,value)

    result=Point_Add(k_value,value)

    print("根据签名推出公钥",result)

mod_value = 19
a = 2
b = 2
G=[7,1]
k=4
message="00460108"
#print(Point_Add([5,1],G))
#print(Multi(k,G))
d=5
r,sig=sign(message,G,d,k)
P = Multi(d, G)
print("公钥为",P)
#print((r,s))
verify(message,G,r,sig,P)
deduce_pubkey(sig,r,k,G)