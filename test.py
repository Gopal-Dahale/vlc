from dahuffman import HuffmanCodec
import ast

filename = 'message.txt'
f = open(filename, 'r')
msg = f.read()

codec = HuffmanCodec.from_data(msg)
encoded_msg = codec.encode(msg)

print(str(codec.get_code_table()))