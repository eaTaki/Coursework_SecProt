import time


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
            node.count = modifier_func(node.count)
            self.modify_node_value(node.left, modifier_func)
            self.modify_node_value(node.right, modifier_func)
        return time.perf_counter() - t0
    

    def encrypt(self, keys):
        self._encrypt(self.root, keys)

    def _encrypt(self, node, keys):
        if node is None:
            return

        node.elGamal = keys.pop()
        node.count = node.elGamal.enc(node.count)

        self._encrypt(node.left, keys)
        self._encrypt(node.right, keys)

    def query_interval(self, interval):
        return self._query_interval(self.root, interval)

    def _query_interval(self, node, interval):
        if node is None:
            return 0

        if interval[0] <= node.min and interval[1] >= node.max:
            return node.count if node.elGamal is None else node.elGamal.dec(node.count)

        if interval[0] > node.max or interval[1] < node.min:
            return 0

        return self._query_interval(node.left, interval) + self._query_interval(node.right, interval)
    
    def get_interval(self, interval=None, count=True):
        if interval is None:
            interval = (self.root.min, self.root.max)
        return self._get_interval(self.root, interval, count)

    def _get_interval(self, node, interval, count=True):
        """
        returns a list of all counts in the tree within the given interval
        """
        if node is None:
            return []

        if interval[0] > node.max or interval[1] < node.min:
            return []

        results = []
        if interval[0] <= node.min and interval[1] >= node.max:
            results.append(node.count if count else node)
        else:
            results.extend(self._get_interval(node.left, interval, count))
            results.extend(self._get_interval(node.right, interval, count))

        return results