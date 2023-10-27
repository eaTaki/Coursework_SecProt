import numpy as np
from mife import MIFE
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import Crypto.Util.number as CUN
from util import generate_gp
import concurrent.futures
from mife import ElGamal


class Node:
    def __init__(self, min_val, max_val):
        self.min = min_val
        self.max = max_val
        self.count = 0
        self.left = None
        self.right = None
        self.elGamal = None

    def print(self):
        if isinstance(self.count, int):
            return self.count
        elif isinstance(self.count, float):
            return round(self.count, 2)
        elif isinstance(self.count, tuple):
            return f"{str(self.count[0])[:2]} | {str(round(self.count[1], 2))[:2]}"
        else:
            return None
        


class BinaryRangeTree:
    def __init__(self, size, x):
        self.root = self._build_tree(1, size)
        [self.insert_data(i) for i in x]

    def _build_tree(self, min_val, max_val):
        if min_val == max_val:
            node = Node(min_val, max_val)
            node.count = 0
            return node

        mid = (min_val + max_val) // 2
        left_node = self._build_tree(min_val, mid)
        right_node = self._build_tree(mid + 1, max_val)

        node = Node(min_val, max_val)
        node.count = left_node.count + right_node.count
        node.left = left_node
        node.right = right_node

        return node
    
    def insert_data(self, data):
        self._insert_data(self.root, data)

    def _insert_data(self, node, data):
        if node is None:
            return

        if node.min <= data <= node.max:
            node.count += 1
            self._insert_data(node.left, data)
            self._insert_data(node.right, data)

    def modify_node_value(self, node, modifier_func):
        t0 = time.perf_counter()
        if node is not None:
            # Modify the node's value using the provided lambda function
            node.count = modifier_func(node.count)
            # Recursively modify values of left and right subtrees
            self.modify_node_value(node.left, modifier_func)
            self.modify_node_value(node.right, modifier_func)
        return time.perf_counter() - t0
    

    def encrypt(self, keys):
        self._encrypt(self.root, keys)

    def _encrypt(self, node, keys):
        if node is None:
            return

        # Encrypt the node's count using the provided ElGamal instance
        node.elGamal = keys.pop()
        node.count = node.elGamal.enc(node.count)

        # Recursively encrypt the left and right subtrees
        self._encrypt(node.left, keys)
        self._encrypt(node.right, keys)

    def query_interval(self, interval):
        return self._query_interval(self.root, interval)

    def _query_interval(self, node, interval):
        # If the node is None, return 0
        if node is None:
            return 0

        # If the interval of the node is contained in the query interval, return the count of the node
        if interval[0] <= node.min and interval[1] >= node.max:
            return node.count if node.elGamal is None else node.elGamal.dec(node.count)

        # If the interval of the node is disjoint with the query interval, return 0
        if interval[0] > node.max or interval[1] < node.min:
            return 0

        # If the interval of the node overlaps with the query interval, recursively call the function
        return self._query_interval(node.left, interval) + self._query_interval(node.right, interval)