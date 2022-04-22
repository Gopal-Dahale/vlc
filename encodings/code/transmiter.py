# import RPi.GPIO as GPIO
import ast
from huffman import Huffman
from run_length import run_length_encode, run_length_transmit
import time
from utils import time_period, transmit_byte, print_stats, fragment_bits, prepare_packet
import argparse
import pyae

# GPIO.setmode(GPIO.BOARD)
data_pin = 12
# GPIO.setup(data_pin, GPIO.OUT, initial=0)

filename = './message.txt'
f = open(filename, 'r')
msg = f.read()
len_msg = len(msg)
max_payload = 32  # bits
max_bits_processing = 64  # bits


def simple_transmission(encoded_msg, max_payload, max_bits_processing):
    """Simple Transmission without any encoding

    Args:
        encoded_msg (str): Boolean string
        max_payload (int): Maxiumm number of bits in the payload of a packet
        max_bits_processing (int): Maxiumum number of bits in a fragment

    Returns:
        float: Time taken for transmission
    """
    start = time.time()
    len_encoded_msg = len(encoded_msg)
    index = 0  # Keeps track of bits of a fragment
    print('Starting transmission\n')

    while (index < len_encoded_msg):
        fragment = fragment_bits(encoded_msg, index, len_encoded_msg,
                                 max_bits_processing)  # Create a fragment

        print("FRAGMENT", fragment)
        print("LEN FRAGMENT", len(fragment))

        index += max_bits_processing
        i = 0

        while (i < len(fragment)):
            print('Sending packet')

            packet = prepare_packet(fragment, 1, i,
                                    max_payload)  # Create a packet
            print("PACKET", packet)
            len_packet = len(packet)

            # Transmit bytes of the packet
            for k in range(0, len_packet, 8):
                if (k + 8 < len_packet):
                    byte = int(packet[k:k + 8], 2)
                else:
                    byte = int(packet[k:], 2)
                transmit_byte(byte)

            i += max_payload

    end = time.time()
    return end - start


def run():

    # Simple parser to parse type of encoding
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=str)
    args = parser.parse_args()
    encoding = args.e

    if encoding == 'huff':

        # Huffman Encoding
        huff = Huffman()
        encoded_msg, _ = huff.Huffman_Encoding(msg)
        len_encoded_msg = len(encoded_msg)
    elif encoding == 'rle':

        # Run length encoding
        out = run_length_encode(msg)
        encoded_msg = "".join([bin(ord(char))[2:].zfill(8) for char in out
                              ])  # Convert out to binary string
    elif encoding == 'atm':

        # Arithmetic Encoding
        # Create Frequency table
        frequency_table = {}
        for ch in msg:
            if ch in frequency_table:
                frequency_table[ch] += 1
            else:
                frequency_table[ch] = 1

        # Encode message
        AE = pyae.ArithmeticEncoding(frequency_table=frequency_table,
                                     save_stages=False)
        table_bits = AE.frequency_table_to_bits()  # Convert table to bit string

        encoded_msg, _, interval_min_value, interval_max_value = AE.encode(
            msg=msg, probability_table=AE.probability_table)  # Encode message

        # Get the binary code out of the floating-point value
        binary_code, _ = AE.encode_binary(float_interval_min=interval_min_value,
                                          float_interval_max=interval_max_value)

        encoded_msg = binary_code[2:]  # remove decimal point
    else:
        # No Encoding scheme
        encoded_msg = ''.join([bin(ord(char))[2:].zfill(8) for char in msg])

    # Synchronize

    # Transmit HIGH for some period of time
    # and then transmit LOW for the reciever
    # to detect the start of the message

    sync_time = 10 * time_period
    HIGH = 255
    LOW = 0
    start = time.time()

    #send high
    while (time.time() - start < sync_time):
        transmit_byte(HIGH)

    #send low for neg edge
    transmit_byte(LOW)  # start of message
    time.sleep(time_period)

    iterations = 1
    if encoding == 'huff':
        for i in range(iterations):
            duration = huff.Huffman_Transmit(encoded_msg, max_payload,
                                             max_bits_processing)
            print_stats(duration, len_msg)
    elif encoding == 'rle':
        for i in range(iterations):
            duration = run_length_transmit(encoded_msg, max_payload,
                                           max_bits_processing)
            print_stats(duration, len_msg)
    elif encoding == 'atm':
        for i in range(iterations):
            duration = AE.arithmetic_transmit(table_bits, encoded_msg,
                                              max_payload, max_bits_processing)
            print_stats(duration, len_msg)
    else:
        for i in range(iterations):
            duration = simple_transmission(encoded_msg, max_payload,
                                           max_bits_processing)


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    # GPIO.cleanup()
    f.close()
