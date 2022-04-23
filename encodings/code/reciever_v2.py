import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from utils import threshold, time_period
import RPi.GPIO as GPIO

HIGH = 275
LOW = 250
MID = 300

# data_pin = 12
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(data_pin, GPIO.IN)

# Software SPI configuration:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
channel = 0
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


def return_bit(x):
    # print('return bits',abs(x-HIGH),abs(x-LOW))
    '''
    print('X',x)
    return (abs(x-HIGH)<abs(x-LOW))
    '''
    
    return (x>MID)
      
        
        

def run():
    print('Reading MCP3008 values, press Ctrl-C to quit...')

    ################# TEST START ######################
    # file = open('transmit_out.txt', 'r')
    # res = file.read()
    # print(res)
    # index = 0
    ################# TEST END ######################
    x = 0

    # Recieve the message

    # Recieve HIGH for some period of time
    # and then recieve LOW for the reciever
    # to detect the start of the message
    
    while True:
        x = mcp.read_adc(channel)
        # x = int(res[index])
        # index += 1

        # detect high
        print(x)
        if return_bit(x):
            x = mcp.read_adc(channel)
            time.sleep(time_period/10)
            #print('positive detected')

            # loop until low detected
            while True:
                x = mcp.read_adc(channel)
                print(x)
                if (return_bit(x) == 0):
                    break

            # 0 detected after detecting 1
            # wait for 1 T and sample
            #print('neg edge detected')
            time.sleep(time_period *1)
            # index += 7
            break
    
    
    
    # Recieve the message
    count = 8
    byte = 0
    string = ''  # Holds the message in bits
    table_string = ''  # Holds the table in bits
    #print('ready for reception')
    while True:
        x = mcp.read_adc(channel)
        print('ADC',x)
        x = return_bit(x)
        byte += (x << (count - 1))
        print('bit',x)
        count -= 1      
        # A byte is recieved
        if (count == 0):
            count = 8
            print('BYTE', byte)
            type_payload = (byte>>7)
            len_payload = (byte & 0x7F)
            remaining_bits = 32
            while remaining_bits:
				x = mcp.read_adc(channel)
				x = return_bit(x)
				if type_payload:
					string += str(x)
					print(str(x))
				else:
					table_string += str(x)
				remaining_bits -= 1
				time.sleep(time_period)
try:
    run()
except KeyboardInterrupt:
    pass
finally:
    pass
    
    
  
