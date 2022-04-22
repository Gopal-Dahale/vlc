from turtle import st
# import RPi.GPIO as GPIO
import ast
from huffman import Huffman
from run_length import run_length_encode, run_length_transmit
import time
from utils import time_period, transmit_byte, print_stats
import argparse

# GPIO.setmode(GPIO.BOARD)
data_pin = 12
# GPIO.setup(data_pin, GPIO.OUT, initial=0)

filename = './message.txt'
f = open(filename, 'r')
msg = f.read()
len_msg = len(msg)
max_payload = 32  # bits
max_bits_processing = 64  # bits


def run():

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=str)
    args = parser.parse_args()
    encoding = args.e
    if encoding == 'huff':
        # Encode msg
        huff = Huffman()
        encoded_msg, _ = huff.Huffman_Encoding(msg)
        len_encoded_msg = len(encoded_msg)
    elif encoding == 'rle':
        out = run_length_encode(msg)
        encoded_msg = "".join([bin(ord(char))[2:].zfill(8) for char in out])

        # print(run_length_decode(encoded_msg))

    print('ENCODED MSG', encoded_msg)
    print("LEN ENCODED MSG", len(encoded_msg))

    # for i in range(len_encoded_msg):
    #     if i % max_bits_processing == 0:
    #         print('__', end='')
    #     print(encoded_msg[i], end='')
    # print('\n')
    # synchronize

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


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    # GPIO.cleanup()
    f.close()
