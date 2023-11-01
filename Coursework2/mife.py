import numpy as np
import random
import concurrent.futures
from utils import generate_gp, generate_keys
from utils import discrete_log





class ElGamal():
    def __init__(self, nbits=1024, sk=None, pk=None, G=None, P=None):

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
    
    def enc(self, m, mode='additive', r=None):
        assert mode in ['multiplicative', 'additive'], "Mode must be either 'multiplicative' or 'additive'"

        r = random.randint(1, self.p-1) if r is None else r
        c1 = pow(self.g, r, self.p)
        if mode == 'additive':
            c2 = (pow(self.g, int(m), self.p) * pow(self.pk, r, self.p)) % self.p
        else:
            c2 = (int(m) * pow(self.pk, r, self.p)) % self.p
        return c1, c2
    
    def dec(self, c, mode='additive'):
        assert mode in ['multiplicative', 'additive'], "Mode must be either 'multiplicative' or 'additive'"

        if not hasattr(self, 'pk'):
                    raise Exception("Public key not set")

        c1, c2 = c
        if mode == 'additive':
            return discrete_log(20, self.g, pow(c1, -self.sk, self.p) * c2 % self.p, self.p)
        else:
            return pow(c1, -self.sk, self.p) * c2 % self.p
            


class MIFE():
    def __init__(self, N = 1, nbits=1024, G = None, P = None) -> None:
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

        # self.r = random.randint(1, self.P-1)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ElGamal, nbits=nbits, G=G, P=P) for _ in range(2**(N+1)-1)]
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
            futures = [executor.submit(self.PKE[i].enc, x[i]) for i in range(self.N)]
            return [f.result() for f in futures]

    def dec_l1(self, c):
        """
        The decryption algorithm takes as input the functional key sk_l1
        and an encrypted vector c and outputs PKE.Dec(sk_l1, prod^n_i=1 ci)
        """
        c = np.prod(c, axis=0)
        c = [c[0] % self.P, c[1] % self.P]
        return self.PKE_l1.dec((int(c[0]), int(c[1])))
        
