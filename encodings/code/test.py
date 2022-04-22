from huffman import Huffman
from run_length import run_length_encode, run_length_decode

filename = './message.txt'
f = open(filename, 'r')
msg = f.read()

out = run_length_encode(msg)
encoded_msg = "".join([bin(ord(char))[2:].zfill(8) for char in out])
len_encoded_msg = len(encoded_msg)

recieved_msg = '001100010011100001100111001100100011000101110100001100010011011101111001'
print(encoded_msg == recieved_msg)
# print(huff.Huffman_Decoding(recieved_msg))

# RLE
# res = ''
# for k in range(0, len_encoded_msg, 8):
#     res += chr(int(recieved_msg[k:k + 8], 2))
# print(run_length_decode(res))