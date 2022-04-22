from huffman import Huffman
from run_length import run_length_encode, run_length_decode
import pyae

filename = './message.txt'
f = open(filename, 'r')
msg = f.read()

frequency_table = {}
for ch in msg:
    if ch in frequency_table:
        frequency_table[ch] += 1
    else:
        frequency_table[ch] = 1
AE = pyae.ArithmeticEncoding(frequency_table=frequency_table, save_stages=False)
table_bits = AE.frequency_table_to_bits()

encoded_msg, _, interval_min_value, interval_max_value = AE.encode(
    msg=msg, probability_table=AE.probability_table)

# Get the binary code out of the floating-point value
binary_code, _ = AE.encode_binary(float_interval_min=interval_min_value,
                                  float_interval_max=interval_max_value)

encoded_msg = binary_code[2:]  # remove decimal point

recieved_bits_table = '011001110000000000010010011101000000000000010101011110010000000000010001'

recieved_bits_msg = '00000000000000000000000000000010111101100111001001000111001011110011010110011011101001010000'

print(recieved_bits_table == table_bits)
print(recieved_bits_msg == encoded_msg)
print(recieved_bits_msg)
print(encoded_msg)
