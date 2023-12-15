import unittest
import random
import numpy as np
from elGamal import ElGamal
from utils import get_GP, enc_gamal_additive
from entities import Curator


N_BITS = 4
N_INSTANCES = 3
G, P = get_GP(load_file="Coursework2/gp.txt", nbits=1024)

class TestElGamal(unittest.TestCase):

    def test_enc_dec(self):

        elGamal = ElGamal(nbits=1024, G=G, P=P)
        m = int(random.randint(1, 100))
        self.assertEqual(m, elGamal.dec(elGamal.enc(m)))

    def test_lch(self):
        # Test Linear Congruence Homomorphism (LCH) (pg. 18)

        r = random.randint(1, P-1)
        elGamal1, elGamal2 = ElGamal(G=G, P=P), ElGamal(G=G, P=P)
        m1, m2 = random.randint(1, 100), random.randint(1, 100)

        enc = [elGamal1.enc(m1, r=r), elGamal2.enc(m2, r=r)]

        c1 = enc[0][0]*enc[1][0] % P, enc[0][1]*enc[1][1] % P
        c2 = enc_gamal_additive((m1 + m2)%P, (elGamal1.pk*elGamal2.pk)%P, G, P, r=r)

        self.assertEqual(c1[1], c2[1])

    def test_lkh(self):
        # Test Linear Key Homomorphism (LKH) (pg. 18)

        r = random.randint(1, P-1)
        elGamal1, elGamal2 = ElGamal(G=G, P=P), ElGamal(G=G, P=P)

        elGamal3 = ElGamal(G=G, P=P, sk=(elGamal1.sk + elGamal2.sk)%P, pk=(elGamal1.pk*elGamal2.pk)%P)

        m = random.randint(1, 100)

        self.assertEqual(elGamal3.dec(elGamal3.enc(m, r=r)), m)


class TestCurator(unittest.TestCase):
    def setUp(self):

        self.N = 5
        x = np.random.randint(1, 2**self.N+1, 100)
        self.curator = Curator(self.N, G=G, P=P, x=x)

        self.interval = np.random.randint(1, 2**self.N+1, 2)
        self.interval.sort()

        self.query = len([i for i in x if self.interval[0] <= i <= self.interval[1]])

    def test_add_noise(self):
        epsilon = 0.5
        self.curator.add_noise(epsilon)
        self.assertTrue(isinstance(self.curator.times["addNoise"], float))

    def test_encrypt(self):
        self.curator.encrypt()
        self.assertTrue(isinstance(self.curator.times["encrypt"], float))

    def test_read_without_f_key(self):
        result = self.curator.read(self.interval)
        self.assertEqual(result, self.query)

    def test_read_with_f_key(self):
        result = self.curator.read(self.interval, f_key=True)
        self.assertEqual(result, self.query)
        


if __name__ == '__main__':
    unittest.main()