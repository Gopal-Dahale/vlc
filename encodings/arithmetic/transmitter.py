from base64 import encode
from turtle import st
import RPi.GPIO as GPIO
import ast
from huffman import Huffman
import time
from encodings.huffman.utils import fragment_bytes, prepare_packet, print_stats
import ast
import pyae

GPIO.setmode(GPIO.BOARD)
data_pin = 12
GPIO.setup(data_pin, GPIO.OUT, initial=0)

filename = 'message.txt'
f = open(filename, 'r')
msg = f.read()
time_period = 0.005  # seconds
len_msg = len(msg)
max_payload = 4  # bytes
max_bytes_processing = 40  # bytes


def transmit_byte(byte):
    # bit_stream = byte
    # print(bit_stream)
    i = 0
    while (i < 8):
        print(1 if byte & (1 << i) else 0, end='')
        # GPIO.output(data_pin, byte & (1 << i))
        time.sleep(time_period)
        i += 1
    # print('\n')


def run():

    # Encode msg
    frequency_table = {}
    for ch in msg:
        if ch in frequency_table:
            frequency_table[ch] += 1
        else:
            frequency_table[ch] = 1

    AE = pyae.ArithmeticEncoding(frequency_table=frequency_table,
                                 save_stages=False)
    # Encode the message
    encoded_msg, encoder, interval_min_value, interval_max_value = AE.encode(
        msg=msg, probability_table=AE.probability_table)
    print("Encoded Message: {msg}".format(msg=encoded_msg))

    # Get the binary code out of the floating-point value
    binary_code, encoder_binary = AE.encode_binary(
        float_interval_min=interval_min_value,
        float_interval_max=interval_max_value)
    print("The binary code is: {binary_code}".format(binary_code=binary_code))

    encoded_msg = binary_code[2:]  # remove decimal point
    table = str(frequency_table)
    len_table = len(table)
    len_encoded_msg = len(encoded_msg)

    # synchronize

    # Transmit HIGH for some period of time
    # and then transmit LOW for the reciever
    # to detect the start of the message
    sync_time = 10 * time_period
    HIGH = chr(255)
    LOW = chr(0)
    start = time.time()

    #send high
    while (time.time() - start < sync_time):
        transmit_byte(HIGH)

    #send low for neg edge
    transmit_byte(LOW)  # start of message
    time.sleep(time_period)

    # Transmit table
    iterations = 1
    for i in range(iterations):

        index = 0
        start = time.time()
        print('Starting transmission\n')
        while (index < len_table):

            fragment = fragment_bytes(table, index, max_bytes_processing)
            index += max_bytes_processing
            i = 0
            while (i < len(fragment)):
                print('sending packet')
                packet = prepare_packet(fragment, 1, i, max_payload)
                print(packet)
                for byte in packet:
                    transmit_byte(byte)

                i += max_payload

        end = time.time()
        print_stats(end - start, len_msg)

    # Transmit msg
    for i in range(iterations):

        index = 0
        start = time.time()
        print('Starting transmission\n')
        while (index < len_encoded_msg):

            fragment = fragment_bytes(encoded_msg, index, max_bytes_processing)
            index += max_bytes_processing
            i = 0
            while (i < len(fragment)):
                print('sending packet')
                packet = prepare_packet(fragment, 1, i, max_payload)
                print(packet)
                for byte in packet:
                    transmit_byte(byte)

                i += max_payload

        end = time.time()
        print_stats(end - start, len_msg)


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    f.close()
