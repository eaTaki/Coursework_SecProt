import numpy as np
from mife import MIFE
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import Crypto.Util.number as CUN
from util import generate_gp
import concurrent.futures
from mife import ElGamal
from range_tree import BinaryRangeTree
    





class Curator():
    def __init__(self, N, x = None, nbits=1024, G = None, P = None):

        times = {}

        # Generate a G group and a P prime
        G, P = generate_gp(nbits=nbits) if (G is None or P is None) else (G, P)


        # Generate and populate the binary range tree
        t0 = time.perf_counter()
        self.T = BinaryRangeTree(2**N, x)
        times["generateAndPopulate"] = (time.perf_counter() - t0)

        # Generate the keys
        t0 = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ElGamal, nbits=nbits, G=G, P=P) for _ in range(2**(N+1)-1)]
            self.keys = [f.result() for f in futures]
        times["generateKeys"] = time.time() - t0

        self.N = N
        self.times = times
        
    def add_noise(self, epsilon):
        insert_noise = lambda x: x + np.random.laplace(0, 1/epsilon)
        self.times["addNoise"] = self.T.modify_node_value(self.T.root, insert_noise)

    def encrypt(self):
        t0 = time.time()
        self.T.encrypt(self.keys)
        self.times["encrypt"] = time.time() - t0

    

    def update(self, data):
        if hasattr(data, "__iter__"):
            for d in data:
                self.T.insert_data(d)
        else:  
            self.T.insert_data(data)

    def read(self, start, end):
        return self.T.query_interval((start, end))