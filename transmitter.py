from turtle import st
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
data_pin = 12
GPIO.setup(data_pin, GPIO.OUT, initial=0)

filename = 'message.txt'
f = open(filename, 'r')
msg = f.read()
time_period = 0.05  # seconds


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

    # Transmit the message
    iterations = 4  # number of times to transmit the message
    for i in range(iterations):
        start = time.time()
        print('Starting transmission\n')
        for msg_byte in msg:
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
