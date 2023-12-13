import numpy as np
import time
from mife import MIFE
from range_tree import BinaryRangeTree
from utils import dec_gamal_additive, generate_gp
import random
    
def generate_f_key(msk, P):
    return msk.pop()+generate_f_key(msk, P)%P if msk else 0
    # return sum(msk)%P




class Curator():
    def __init__(self, N, x = None, nbits=1024, G = None, P = None, r=None):

        times = {}

        if G is None or P is None:
            G, P = generate_gp(nbits=nbits)
        self.G, self.P = G, P

        self.r = random.randint(2, P-2) if r is None else r


        # Generate and populate the binary range tree
        t0 = time.perf_counter()
        self.T = BinaryRangeTree(2**N, x)
        times["generateAndPopulate"] = (time.perf_counter() - t0)

        # Generate the keys
        t0 = time.time()
        self.mife = MIFE(N, nbits, G, P, self.r)
        times["generateKeys"] = time.time() - t0

        self.N = N
        self.times = times
        
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
            if type(self.T.root.count ) is not tuple:
                # print("Tree not encrypted")
                self.encrypt()
            nodes = self.T.get_interval(interval, count=False)
            f_key = generate_f_key([node.elGamal.sk for node in nodes], self.P)
            c = np.prod([node.count[1] for node in nodes])%self.P
            return dec_gamal_additive((pow(self.G, self.r, self.P), c), f_key, self.G, self.P)
        else:
            return self.T.query_interval(interval)