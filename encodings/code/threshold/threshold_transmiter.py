from turtle import st
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
data_pin = 3
GPIO.setup(data_pin, GPIO.OUT, initial=0)

time_period = 0.2  # seconds

def run():
    msg = '10111111111'*30
    
    # Synchronize

    # Transmit HIGH for some period of time
    # and then transmit LOW for the reciever
    # to detect the start of the message

    sync_time = 2 * time_period
    HIGH = 255
    LOW = 0
    start = time.time()

    #send high
    while (time.time() - start < sync_time):
        GPIO.output(data_pin, 1)

    #send low for neg edge
    
    GPIO.output(data_pin, 0)
     # start of message
    time.sleep(time_period *1)
    
    
    # Transmit the message
    iterations = 1  # number of times to transmit the message
    for i in range(iterations):
        start = time.time()
        print('Starting transmission\n')
        for j in msg:
            print(j)
            GPIO.output(data_pin, int(j))
            time.sleep(time_period)
        end = time.time()


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
