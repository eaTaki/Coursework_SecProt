import numpy as np
import random
import concurrent.futures
from utils import generate_gp
from elGamal import ElGamal




        
            


class MIFE():
    def __init__(self, N = 1, nbits=1024, G = None, P = None, r = None) -> None:
        """
        The setup algorithm invokes the PKE's key generation algo-
        rithm Gen and generates n public/private key pairs
        The public keys are then used to create and output a master public/private
        key pair
        """
        self.N = N

        if G is None or P is None:
            G, P = generate_gp(nbits=nbits)
        self.G, self.P = G, P

        self.r = random.randint(2, P-2) if r is None else r

        # self.r = random.randint(1, self.P-1)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ElGamal, nbits=nbits, G=G, P=P, r=r) for _ in range(2**(N+1)-1)]
            self.PKE = [f.result() for f in futures]

        
        self.mpk = [i.pk for i in self.PKE]
        self.msk = [i.sk for i in self.PKE]

        """
        The key generation algorithm, takes as input the master secret
        key msk and outputs a functional key sk_l1 = sum^n_i=1 ski  
        """
        pk_l1 = int(np.prod(self.mpk))%self.P
        sk_l1 = int(np.sum(self.msk))%self.P
        self.PKE_l1 = ElGamal(nbits = nbits, sk = sk_l1, pk=pk_l1, G = self.G, P = self.P) 
    
    def enc(self, x):
        """
        Enc(mpk, x): The encryption algorithm Enc, takes as input the master public
        key mpk and a vector x and outputs c = {c1, . . . , cn}, where ci = Enc(pki, xi)
        """

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.PKE[i].enc, x[i], self.r) for i in range(self.N)]
            return [f.result() for f in futures]
        
