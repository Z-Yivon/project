import time
import random
from gmssl import sm3, func

def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串
  """
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789`~!@#$%^&*'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str


if __name__ == '__main__':
    a = dict()
    n = 8   # 碰撞前 n*4 比特
    # 数据和加密后数据为bytes类型
    data = b"202100460108" # bytes类型
    h_1 = sm3.sm3_hash(func.bytes_to_list(data))
    hash1 = h_1[:n]
    start = time.time()
    hash2 = ""
    while(hash1 != hash2):
        s = generate_random_str()
        ss = bytes(s.encode())
        h_2 = sm3.sm3_hash(func.bytes_to_list(ss))
        hash2 = h_2[:n]
    end = time.time()
    print("\nFind the collision!(",n*4,"bits)\n")
    print("str1:",data,"\nhash(str1):",h_1)
    print("str2:",ss,"\nhash(str2):", h_2)
    print("Running time:",end-start,"seconds")
