# Testing hashing sequences
# Tanner Fry
# tefnq2@mst.edu
import random
# Basic hash principle, a function that takes in input value, and from that input creates an output value deterministic of the input value.

def hash_me(int):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_length = 128
    hashed = ''
    random.seed(int)  # Output value is now deterministic of the input
    for i in range(hash_length):
        rand_num = random.randint(0, 9)
        # Even then odd
        if i % 2 is 0:
            hashed = hashed + str(alphabet[rand_num])
        else:
            hashed = hashed + str(rand_num)
    return hashed


hash = hash_me(input('Int: '))
print(hash)