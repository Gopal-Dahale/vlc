import pickle


# A Huffman Tree Node
class Node:

    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob  # probability of symbol
        self.symbol = symbol  # symbol
        self.left = left  # left node
        self.right = right  # right node
        self.code = ''  # tree direction (0/1)


class Huffman:

    def __init__(self):
        self.codes = dict()
        handle = open('huff_table.pickle', 'rb')
        self.nodes0 = pickle.load(handle)
        self.huffman_encoding = self.Calculate_Codes(self.nodes0)

    def Calculate_Codes(self, node, val=''):
        """ A helper function to print the codes of symbols by traveling Huffman Tree"""
        # huffman code for current node
        newVal = val + str(node.code)

        if (node.left):
            self.Calculate_Codes(node.left, newVal)
        if (node.right):
            self.Calculate_Codes(node.right, newVal)

        if (not node.left and not node.right):
            self.codes[node.symbol] = newVal

        return self.codes

    def Calculate_Probability(self, data):
        """ A helper function to calculate the probabilities of symbols in given data"""
        symbols = dict()
        for element in data:
            if symbols.get(element) == None:
                symbols[element] = 1
            else:
                symbols[element] += 1
        return symbols

    def Output_Encoded(self, data, coding):
        """ A helper function to obtain the encoded output"""
        encoding_output = []
        for c in data:
            #  print(coding[c], end = '')
            encoding_output.append(coding[c])

        string = ''.join([str(item) for item in encoding_output])
        return string

    def Total_Gain(self, data, coding):
        """ A helper function to calculate the space difference between compressed and non compressed data"""
        before_compression = len(
            data) * 8  # total bit space to stor the data before compression
        after_compression = 0
        symbols = coding.keys()
        for symbol in symbols:
            count = data.count(symbol)
            after_compression += count * len(
                coding[symbol]
            )  #calculate how many bit is required for that symbol in total
        print("Space usage before compression (in bits):", before_compression)
        print("Space usage after compression (in bits):", after_compression)

    def Huffman_Encoding(self, data):
        self.Total_Gain(data, self.huffman_encoding)
        encoded_output = self.Output_Encoded(data, self.huffman_encoding)
        return encoded_output, self.nodes0

    def Huffman_Decoding(self, encoded_data, huffman_tree):
        tree_head = huffman_tree
        decoded_output = []
        for x in encoded_data:
            if x == '1':
                huffman_tree = huffman_tree.right
            elif x == '0':
                huffman_tree = huffman_tree.left
            try:
                if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                    pass
            except AttributeError:
                decoded_output.append(huffman_tree.symbol)
                huffman_tree = tree_head

        string = ''.join([str(item) for item in decoded_output])
        return string


""" First Test """
data = "AAAAAasdfsadfAAAAAABBsdaasdasdfBBBBsadfasdfBasdfsadfasdCCCCCDDDDEEEF"
print(data)
huff = Huffman()
encoding, tree = huff.Huffman_Encoding(data)
print("Encoded output", encoding)
decoded = huff.Huffman_Decoding(encoding, tree)
print("Decoded Output", decoded)
print(data == decoded)
""" Second Test """