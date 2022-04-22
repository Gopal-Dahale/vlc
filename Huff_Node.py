# A Huffman Tree Node
class Node:

    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob  # probability of symbol
        self.symbol = symbol  # symbol
        self.left = left  # left node
        self.right = right  # right node
        self.code = ''  # tree direction (0/1)