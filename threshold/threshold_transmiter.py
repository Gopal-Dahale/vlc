from turtle import st
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
data_pin = 3
GPIO.setup(data_pin, GPIO.OUT, initial=0)

time_period = 0.2  # seconds

def run():
    msg = '10'*30
    # Transmit the message
    iterations = 1  # number of times to transmit the message
    for i in range(iterations):
        start = time.time()
        print('Starting transmission\n')
        for j in msg:
            print(j, end='')
            GPIO.output(data_pin, int(j))
            time.sleep(time_period)
        print('\n')
        end = time.time()


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
