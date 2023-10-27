from mife import MIFE
from entities import Curator
import copy


"""
Architecture We assume the existence of the following entities:
- Curator (C): C is responsible for creating an encrypted and private database.
C outsources the database to a CSP where it will be stored. Moreover, C
can issue update queries to the CSP update specific entries of the database.
To do so, C keeps locally the latest version of the database.
- Analyst (A): A is an analyst that can perform statistics on the data stored
in the CSP.
- CSP: A cloud service provider that stores an encrypted database. The CSP
releases statistics upon request of the analyst.
"""

class PLM_H():
    """
    PLMH makes use of the MIFE_l1 and a public-key en-
    cryption scheme PKE = (Gen, Enc, Dec) that satisfies the LCH and LKH proper-
    ties. Moreover, the encryption function of PKE must be additively homomorphic.
    PLMH is then defined as PLMH = (Setup, Update, Read).
    """
    def __init__(self, x):
        """
        Setup is a two party protocol between C and the CSP. C outputs a
        complete binary tree T with n nodes and adds Laplacian noise to the content of
        each node. As a next step, C runs MIFE_l1.Setup and generates n public/private
        key pairs (pki, ski) . Finally, C encrypts each node i using a public key pki and
        T is outsourced to the CSP.
        """
        self.C = Curator(x)
        self.T = copy.deepcopy(self.C.T)
        # adding noise to the content of each node
        
    
    def update(self, k, i):
        """
        To update the content of a node, C makes use of the homomorphic property of PKE.Enc. More
        precisely, assuming that C wishes to add a value k to the content of a leaf node
        i, she first finds the path from the root of the tree to the leaf i. For every node
        j in the path, C samples a distinct e_j ~ Lap(1/epsilon') and computes k'_j = k_j + e_j . As
        a next step, C encrypts each k'_j using pk_j . Apart from that, C samples a fresh
        noise em for every other node m of the tree and encrypts it using pkm. Finally,
        for each node of the tree, C sends a pair (n, cn) to the CSP. Upon reception, the
        CSP updates each node i using c_i by computing c'_n = c_n_{old} · c_n, where c_{nold} the
        current content of the node n.
        """
        


