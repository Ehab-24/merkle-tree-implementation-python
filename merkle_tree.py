import hashlib
import logging
from termcolor import colored
from utils import print_event


class MerkleNode:
    def __init__(self, hash_value, content, left, right):
        self.hash = hash_value
        self.content = content
        self.left = left
        self.right = right


class MerkleTree:
    def __init__(self, chunks):
        hashes = [self.hash256(chunk) for chunk in chunks]

        leaves = []
        for i, hash_value in enumerate(hashes):
            leaves.append(MerkleNode(hash_value, chunks[i], None, None))
        self.root = self.create_merkle_root(leaves)

    def create_merkle_root(self, nodes):
        n = len(nodes)
        if n == 2:
            return MerkleNode(
                self.hash256(nodes[0].hash + nodes[1].hash), "", nodes[0], nodes[1]
            )

        half = n // 2
        left = self.create_merkle_root(nodes[:half])
        right = self.create_merkle_root(nodes[half:])

        # Sort nodes in alphabetical order
        if left.hash > right.hash:
            left, right = right, left

        hash_value = self.hash256(left.hash + right.hash)

        return MerkleNode(hash_value, "", left, right)

    @staticmethod
    def hash256(data):
        return hashlib.sha256(data.encode()).hexdigest()

    def print_tree_rec(self, node, level):
        if node is None:
            return

        bullet = f"{level} "
        if level == 0:
            bullet = ""

        node_str = node.hash
        if node.content != "":
            node_str = f"{node.hash} (Leaf)"

        cyan = lambda x: colored(x, "cyan")
        print(level * 2 * " ", f"{cyan(bullet)}{node_str}")

        self.print_tree_rec(node.left, level + 1)
        self.print_tree_rec(node.right, level + 1)

    def print_tree(self):
        print("\nMerkle Tree")
        self.print_tree_rec(self.root, 0)

    def root_hash(self):
        return self.root.hash

    def prove_membership(self, elems):
        current_node = self.root
        for elem in elems:
            if elem.hash != current_node.hash:
                logging.info("found")
                return None

            if elem.direction == "Left":
                current_node = current_node.left
            else:
                current_node = current_node.right

        return current_node

    def find_node(self, node, target_hash):
        if node is None:
            return None
        if node.hash == target_hash:
            return node
        left = self.find_node(node.left, target_hash)
        right = self.find_node(node.right, target_hash)

        if left is not None:
            return left
        return right

    def prove_non_membership(self, hash_value):
        node = self.find_node(self.root, hash_value)
        return node is None
