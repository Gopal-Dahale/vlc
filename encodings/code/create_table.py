# Code to create a huffman table which will we
# available at both transmitter and reciever
# side. This will save time in trasnmission of
# table.

import pickle
from Huff_Node import Node

f = open('julius_caesar.txt')
text = f.read()

# find frequency of each character
freq = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0,
    "E": 0,
    "F": 0,
    "G": 0,
    "H": 0,
    "I": 0,
    "J": 0,
    "K": 0,
    "L": 0,
    "M": 0,
    "N": 0,
    "O": 0,
    "P": 0,
    "Q": 0,
    "R": 0,
    "S": 0,
    "T": 0,
    "U": 0,
    "V": 0,
    "W": 0,
    "X": 0,
    "Y": 0,
    "Z": 0,
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
    'f': 0,
    'g': 0,
    'h': 0,
    'i': 0,
    'j': 0,
    'k': 0,
    'l': 0,
    'm': 0,
    'n': 0,
    'o': 0,
    'p': 0,
    'q': 0,
    'r': 0,
    's': 0,
    't': 0,
    'u': 0,
    'v': 0,
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0,
    ' ': 0,
    '.': 0,
    ',': 0,
    '!': 0,
    '?': 0,
    '\'': 0,
    '"': 0,
    ':': 0,
    ';': 0,
    '-': 0,
    '\n': 0,
    '\t': 0,
    '(': 0,
    ')': 0,
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 0,
    '8': 0,
    '9': 0,
}
for c in text:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1
print(freq)

codes = dict()


def Calculate_Codes(node, val=''):
    """ A helper function to print the codes of symbols by traveling Huffman Tree"""
    # huffman code for current node
    newVal = val + str(node.code)

    if (node.left):
        Calculate_Codes(node.left, newVal)
    if (node.right):
        Calculate_Codes(node.right, newVal)

    if (not node.left and not node.right):
        codes[node.symbol] = newVal

    return codes


symbol_with_probs = freq
symbols = symbol_with_probs.keys()
probabilities = symbol_with_probs.values()
print("symbols: ", symbols)
print("probabilities: ", probabilities)

nodes = []

# converting symbols and probabilities into huffman tree nodes
for symbol in symbols:
    nodes.append(Node(symbol_with_probs.get(symbol), symbol))

while len(nodes) > 1:
    # sort all the nodes in ascending order based on their probability
    nodes = sorted(nodes, key=lambda x: x.prob)
    # for node in nodes:
    #      print(node.symbol, node.prob)

    # pick 2 smallest nodes
    right = nodes[0]
    left = nodes[1]

    left.code = 0
    right.code = 1

    # combine the 2 smallest nodes to create new node
    newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left,
                   right)

    nodes.remove(left)
    nodes.remove(right)
    nodes.append(newNode)

with open('huff_table.pickle', 'wb') as handle:
    pickle.dump(nodes[0], handle)
