import unittest
import random
import numpy as np
from mife import ElGamal, MIFE
from utils import generate_gp, l1_norm

N_BITS = 4
N_INSTANCES = 3
G, P = generate_gp(N_BITS)

print(f"p = {P} | g = {G}")

class TestElGamal(unittest.TestCase):

    def test_enc_dec(self):

        elGamal = ElGamal(nbits=16)

        x = int(random.randint(1, P-1))
        c1, c2 = elGamal.enc(x)
        x_dec = elGamal.dec((c1, c2))

        self.assertEqual(x, x_dec)

    def test_lch(self):
        # Test Linear Congruence Homomorphism (LCH) (pg. 18)

        elGamal1, elGamal2 = ElGamal(g=G, p=P), ElGamal(g=G, p=P)

        x1, x2 = random.randint(1, P-1), random.randint(1, P-1)

        elGamal3 = ElGamal(g=G, p=P)
        elGamal3.pk = (elGamal1.pk * elGamal2.pk) % P

        c1 = np.prod([elGamal1.enc(x1), elGamal2.enc(x2)], axis=1)
        c1 = (c1[0] % P, c1[1] % P)
        c2 = elGamal3.enc(x1+x2)

        self.assertEqual(c1, c2)

    def test_lkh(self):
        # Test Linear Key Homomorphism (LKH)

        elGamal1, elGamal2 = ElGamal(), ElGamal()

        # Encrypt a plaintext using two different public keys
        plain_text = random.randint(1, P-1)
        c1, c2 = elGamal1.enc(plain_text)
        c3, c4 = elGamal2.enc(plain_text)

        # Decrypt the ciphertexts using the combined public key
        decrypted_combined1 = elGamal1.dec(c1, c2)
        decrypted_combined2 = elGamal2.dec(c3, c4)

        # The decrypted results should be the same
        self.assertEqual(decrypted_combined1, decrypted_combined2)

class TestMIFE(unittest.TestCase):
    def setUp(self):
        self.mife = MIFE(G, P, 3)
        self.mpk = self.mife.mpk
        self.msk = self.mife.msk
        self.x = [1, 2, 3]
        self.c = self.mife.enc(self.x)

    def test_enc(self):
        c = self.mife.enc(self.x)
        self.assertEqual(len(c), self.mife.N)
        for i in range(self.mife.N):
            self.assertIsNotNone(c[i])

    def test_dec_l1(self):
        x_dec = self.mife.dec_l1(self.c)
        l1 = l1_norm(P, self.x)
        self.assertEqual(x_dec, l1)

if __name__ == '__main__':
    unittest.main()