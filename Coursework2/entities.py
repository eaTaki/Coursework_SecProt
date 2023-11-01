import numpy as np
import time
from mife import MIFE
from range_tree import BinaryRangeTree
from utils import dec_gamal_additive
    





class Curator():
    def __init__(self, N, x = None, nbits=1024, G = None, P = None):

        times = {}


        # Generate and populate the binary range tree
        t0 = time.perf_counter()
        self.T = BinaryRangeTree(2**N, x)
        times["generateAndPopulate"] = (time.perf_counter() - t0)

        # Generate the keys
        t0 = time.time()
        self.mife = MIFE(N, nbits, G, P)
        times["generateKeys"] = time.time() - t0

        self.N = N
        self.times = times
        self.G, self.P = G, P
        
    def add_noise(self, epsilon):
        insert_noise = lambda x: x + np.random.laplace(0, 1/epsilon)
        self.times["addNoise"] = self.T.modify_node_value(self.T.root, insert_noise)

    def encrypt(self):
        t0 = time.time()
        self.T.encrypt(self.mife.PKE)
        self.times["encrypt"] = time.time() - t0

    

    def update(self, data):
        if hasattr(data, "__iter__"):
            for d in data:
                self.T.insert_data(d)
        else:  
            self.T.insert_data(data)

    def read(self, interval, f_key=False):
        if f_key:
            nodes = self.T.get_interval(interval, count=False)
            # func_key = int(np.sum([node.elGamal.sk for node in nodes]))
            c = np.prod([node.count for node in nodes], axis=0).tolist()
            return dec_gamal_additive(c, nodes[0].elGamal.sk, self.G, self.P)
        else:
            return self.T.query_interval(interval)