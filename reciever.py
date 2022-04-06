import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

GPIO.setmode(GPIO.BOARD)  # Circle numbers
data_pin = 12
GPIO.setup(data_pin, GPIO.OUT, initial=0)

# Software SPI configuration:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
channel = 0
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

filename = 'message.txt'
f = open(filename, 'r')
msg = f.read()
time_period = 0.05  # seconds
threshold = 350


def print_stats(duration):
    print('Total bits send: ', len(msg) * 8)
    print('Total time taken(s): ', duration)
    print('Datarate(bps): ', len(msg) * 8 / (duration))


def run():
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    # Recieve the message

    # Recieve HIGH for some period of time
    # and then recieve LOW for the reciever
    # to detect the start of the message
    while True:
        x = mcp.read_adc(channel)
        if x < threshold:
            break

    # Recieve the message


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    f.close()
