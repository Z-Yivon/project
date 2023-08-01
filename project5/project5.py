import hashlib
import numpy as np
import random

class MerkleTree:
    def __init__(self, leaf):
        self.leaf = leaf
        self.root = None
        self.list = []

    # following RFC 6962
    def sha256_leaf(self,value):   # 级联0x00
        return hashlib.sha256((value[0:2] + "00" + value[2:]).encode('utf-8')).hexdigest()

    def sha256_node(self,value):   # 级联0x01
        return hashlib.sha256((value[0:2] + "01" + value[2:]).encode('utf-8')).hexdigest()

    def create(self):
        leaf_hash = []
        count = len(self.leaf)
        for i in range(count):
            hashvalue = self.sha256_leaf(self.leaf[i].value)
            leaf_hash_node = MerkleTreeNode(hashvalue)
            leaf_hash.append(leaf_hash_node)

        # 中间节点是左右子节点级联再按规则hash
        node = []    # 元素是节点
        node.append(leaf_hash)
        if count == 1:    # 根节点就是叶子结点的hash
            self.root = leaf_hash[0]
            return  self.root

        while len(leaf_hash) > 1:
            t = []
            for i in range(0, len(leaf_hash), 2):
                lchild = leaf_hash[i]
                if (i+1)>=len(leaf_hash):
                    parent_hash = self.sha256_node(lchild.value+lchild.value)
                    parent_node = MerkleTreeNode(parent_hash)
                    parent_node.lchild = lchild
                    parent_node.rchild = lchild
                    lchild.parent = parent_node
                    t.append(parent_node)
                else:
                    rchild = leaf_hash[i+1]
                    parent_hash = self.sha256_node(lchild.value+rchild.value)
                    parent_node = MerkleTreeNode(parent_hash)
                    parent_node.lchild = lchild
                    parent_node.rchild = rchild
                    lchild.parent = parent_node
                    rchild.parent = parent_node
                    # node.append(parent_hash)
                    t.append(parent_node)
            leaf_hash = t
        self.root = leaf_hash[0]
        return self.root

    # 中序遍历得到整个Merkle Tree的节点值
    def print_node(self, root):
        if(root == None):
            return
        self.print_node(root.lchild)
        # print(root.value," ")
        self.list.append(root.value)
        self.print_node(root.rchild)
        return self.list

    def proof(self, root, nodevalue):
        list = self.print_node(root)
        if nodevalue in list:   # inclusive
            print("Node:",nodevalue,"  This node is in the Merkle Tree")
        else:          # exclusive
            print("Node:",nodevalue,"  This node is not in the Merkle Tree")


class MerkleTreeNode:
    def __init__(self, value):
        self.lchild = None    # 左子节点
        self.rchild = None    # 右子节点
        self.parent = None    # 父节点
        self.value = value    # 每个节点的哈希值


if __name__ == '__main__':
    leaf_value = np.random.randint(low = 0, high = 10**6, size=10**5)  # 生成10万个随机数作为叶子结点的值
    leaf_hex = [ hex(i) for i in leaf_value ]
    leaf_node = [ MerkleTreeNode(i) for i in leaf_hex ]
    # print(leaf_hex[1][0:2] + "00" + leaf_hex[1][2:])
    mt = MerkleTree(leaf_node)
    root = mt.create()

    print("Root of the Merkle Tree:\n",root.value)
    # print("遍历全部节点")
    # print(mt.print_node(root))

    print("Inclusion and Exclusion Proof")

    mt.proof(root,root.value)
    number1 = hex(random.randint(0,10**6))
    numberhash1 = hashlib.sha256(number1.encode('utf-8')).hexdigest()
    mt.proof(root,numberhash1)

    number2 = hex(random.randint(0,10**6))
    numberhash2 = hashlib.sha256(number2.encode('utf-8')).hexdigest()
    mt.proof(root,numberhash2)

    number3 = leaf_node[1].value
    numberhash3 = hashlib.sha256((number3[0:2] + "00" + number3[2:]).encode('utf-8')).hexdigest()
    mt.proof(root,numberhash3)
