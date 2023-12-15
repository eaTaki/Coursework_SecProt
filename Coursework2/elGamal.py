import numpy as np
import random
import concurrent.futures
from utils import generate_gp, generate_keys, enc_gamal_additive, dec_gamal_additive





class ElGamal():
    def __init__(self, nbits=1024, sk=None, pk=None, G=None, P=None, r=None):

        if G is None or P is None:
            G, P = generate_gp(nbits=nbits)
        self.g, self.p = G, P
        self.nbits = nbits
        if pk is not None or sk is not None:
            if sk is not None:
                self.sk = sk
                self.pk = pow(G, sk, P)
            if pk is not None:
                self.pk = pk
            return
        self.sk, self.pk = generate_keys(G, P)
        if r:
            self.r = r
    
    def enc(self, m, r=None):
        return enc_gamal_additive(m, self.pk, self.g, self.p, (self.r if hasattr(self, 'r') else r))
    
    def dec(self, c):

        if not hasattr(self, 'pk'):
            raise Exception("Public key not set")
        return dec_gamal_additive(c, self.sk, self.g, self.p)
    