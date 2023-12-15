# Multi-Input Functional Encryption for the $|| l_1 ||$ norm
import numpy as np
import multiprocessing
from Crypto.Util import number

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization



def l1_norm(x, P):
    r = 0
    [r := r + i%P for i in x]
    return r%P


def find_gp(result_queue, nbits):
    while True:
        q = number.getPrime(nbits - 1)
        p = 2 * q + 1
        if number.isPrime(p):
            while True:
                g = number.getRandomRange(2, p - 1)
                if pow(g, q, p) == 1 and pow(g, 2, p) != 1:
                    result_queue.put((g, p))
                    return

def generate_gp(nbits=1024, num_processes=4):
    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(num_processes):
        p = multiprocessing.Process(target=find_gp, args=(result_queue, nbits))
        processes.append(p)
        p.start()

    # Wait for a process to finish and return its result
    g, p = result_queue.get()

    # Terminate the other processes
    for process in processes:
        if process.is_alive():
            process.terminate()

    return g, p

def get_GP(load_file=None, nbits=1024):
    if load_file: 
        load_file = 'gp.txt' if type(load_file) == bool else load_file
        # loading the generated values
        with open(load_file, 'r') as f:
            G = int(f.readline().split('=')[1])
            P = int(f.readline().split('=')[1])
    else:
        G, P = generate_gp(nbits=1024, num_processes=8)
        print("G =", G)
        print("P =", P) 
        # saving the generated values
        with open('gp.txt', 'w') as f:
            f.write("G = " + str(G) + "\n")
            f.write("P = " + str(P) + "\n")
    return G, P

def generate_keys(G, P):
    while True:
        x = number.getRandomRange(2, P-2)
        y = pow(G, x, P)
        if y != 1:
            break
    sk = pollard_rho(P-1, lambda x: pow(G, x, P), lambda x: pow(x, 2, P)-1)
    pk = pow(G, sk, P)
    return sk, pk

def generate_keys_(G, P):
    parameters = dh.DHParameterNumbers(P, G).parameters()

    # Generate private key
    private_key = parameters.generate_private_key()

    # Convert the private key to an integer
    sk = private_key.private_numbers().x

    # Convert the public key to an integer
    pk = private_key.public_key().public_numbers().y



    return sk, pk




def pollard_rho(n, f, g):
    x = 2
    y = 2
    d = 1
    while d == 1:
        x = f(x) % n
        y = f(g(y)) % n
        d = int(np.gcd(abs(x-y), n))
    return d



def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("The modular inverse does not exist")
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def plot_tree(tree, title, fontsize=4):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(title)
    max_depth = tree.root.max.bit_length()
    ax.axis('off')
    ax.set_aspect('equal')

    node_positions = {}
    queue = [(tree.root, 1)]
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node, level = queue.pop(0)
            x = 2**(node.max.bit_length() - 1) + node.min*2
            y = max_depth - 2*level + 1
            node_positions[node] = (x, y)
            ax.add_patch(patches.Circle((x, y), radius=0.8, facecolor='white', edgecolor='black'))
            ax.text(x, y, str(node.print()), ha='center', va='center', fontsize=fontsize)
            ax.text(x, y + 1, f"[{node.min}-{node.max}]", ha='center', va='center', fontsize=fontsize)

            if node.left is not None:
                queue.append((node.left, level + 1))
                x1, y1 = node_positions[node]
                x2, y2 = 2**(node.left.max.bit_length() - 1) + node.left.min*2, max_depth - (2*level + 1)
                ax.plot([x1, x2], [y1, y2], color='black', zorder=0, alpha=0.5)
            if node.right is not None:
                queue.append((node.right, level + 1))
                x1, y1 = node_positions[node]
                x2, y2 = 2**(node.right.max.bit_length() - 1) + node.right.min*2, max_depth - (2*level + 1)
                ax.plot([x1, x2], [y1, y2], color='black', zorder=0, alpha=0.5)

    plt.show()


def discrete_log(nbits, base, exp, mod):
    for i in range(2**nbits):
        if pow(base, i, mod) == exp:
            return i
        

def enc_gamal_additive(x, pk, G, P, r=None):
    r = number.getRandomRange(2, P-2) if r is None else r
    c1 = pow(G, r, P)
    c2 = (pow(pk, r, P) * pow(G, int(x), P))%P
    return (c1, c2)

def dec_gamal_additive(c, sk, G, P):
    c1, c2 = c
    return discrete_log(15, G, pow(c1, -sk, P) * c2 % P, P)