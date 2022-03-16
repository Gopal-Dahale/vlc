import RPi.GPIO as GPIO
import time
from dahuffman import HuffmanCodec
import ast

GPIO.setmode(GPIO.BOARD)
data_pin = 12
GPIO.setup(data_pin, GPIO.OUT, initial=0)

filename = 'message.txt'
f = open(filename, 'r')
msg = f.read()
time_period = 0.005  # seconds


def print_stats(duration):
    print('Total bits send: ', len(msg) * 8)
    print('Total time taken(s): ', duration)
    print('Datarate(bps): ', len(msg) * 8 / (duration))


def transmit_byte(byte):
    bit_stream = ord(byte)
    i = 0
    while (i < 8):
        GPIO.output(data_pin, bit_stream & (1 << i))
        time.sleep(time_period)
        i += 1


def run():
    codec = HuffmanCodec.from_data(msg)
    encoded_msg = codec.encode(msg)

    # Transmit codec table
    table = str(codec.get_code_table())
    for byte in table:
        transmit_byte(byte)

    for i in range(4):
        start = time.time()
        print('Starting transmission\n')
        for msg_byte in encoded_msg:
            transmit_byte(msg_byte)
        end = time.time()

        print_stats(end - start)


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    f.close()
