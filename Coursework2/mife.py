import numpy as np
import random
from Crypto.PublicKey import RSA
import concurrent.futures
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from util import generate_gp, generate_keys





class ElGamal():
    def __init__(self, nbits=1024, sk=None, G=None, P=None):

        if G is None or P is None:
            G, P = generate_gp(nbits=nbits)

        if sk is not None:
            self.sk = sk
            self.pk = pow(G, sk, P)

            return
        self.sk, self.pk = generate_keys(G, P)
        self.g, self.p = G, P
    
    def enc(self, m):
        r = random.randint(1, self.p-1)
        c1 = pow(self.g, r, self.p)
        c2 = (int(m) * pow(self.pk, r, self.p)) % self.p
        return (c1, c2)
    
    def dec(self, c):
        c1, c2 = c
        return pow(c1, -self.sk, self.p) * c2 % self.p
        # EL GAMAL ADDITIVE HOMOMORPHISM IS AN INTRACTABLE PROBLEM


class MIFE():
    def __init__(self, n = 1, nbits=1024, G = None, P = None) -> None:
        """
        The setup algorithm invokes the PKE's key generation algo-
        rithm Gen and generates n public/private key pairs
        The public keys are then used to create and output a master public/private
        key pair
        """
        # The g and p parameters must be the same for all ElGamal instances
        self.n = n

        if G is None or P is None:
            G, P = generate_gp(nbits=nbits)

        self.g, self.p = G, P

        # Generate n ElGamal instances in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ElGamal, nbits=nbits, G=G, P=P) for _ in range(n)]
            self.PKE = [f.result() for f in futures]

        
        self.mpk = [i.pk for i in self.PKE]
        self.msk = [i.sk for i in self.PKE]

        # The functional key is the sum of the secret keys
        """
        The key generation algorithm, takes as input the master secret
        key msk and outputs a functional key sk_l1 = sum^n_i=1 ski  
        """
        # Generating ElGamal instance where sk is sum of all sks
        # self.PKE_l1 = ElGamal(sk = l1_norm(self.msk)) 
        # self.fk_l1 = self.PKE_l1.sk
    
    def enc(self, x):
        """
        Enc(mpk, x): The encryption algorithm Enc, takes as input the master public
        key mpk and a vector x and outputs c = {c1, . . . , cn}, where ci = Enc(pki, xi)
        """

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.PKE[i].enc, x[i]) for i in range(self.n)]
            return [f.result() for f in futures]

    def dec_l1(self, c):
        """
        The decryption algorithm takes as input the functional key sk_l1
        and an encrypted vector c and outputs PKE.Dec(sk_l1, prod^n_i=1 ci)
        """
        c = np.prod(c, axis=0)
        return self.PKE_l1.dec(int(c[0]), int(c[1]))
        
