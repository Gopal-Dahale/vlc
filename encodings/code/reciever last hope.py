# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib.pyplot as plt
from utils import threshold, time_period

MID = 500
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
channel = 0
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
filename = 'received_msg.txt'
f = open(filename, 'w')

def return_bit():
    # finds a bit by multiple sampling
    sum_samples = 0
    num_samples = 10
    sample = 0
    
    while sample<num_samples:
        x = mcp.read_adc(channel)
        if(x>MID):
            sum_samples+=1
        time.sleep(time_period/num_samples)
        sample+=1
        
    # print bit determined after multiple samples
    if(sum_samples>=(num_samples/2)):
        bit = 1
        print(1)
    else:
        bit = 0
        print(0)
    sum_samples = 0
    sample = 0
    
    return bit

    
def run():
    # Software SPI configuration:


    # Hardware SPI configuration:
    # SPI_PORT   = 0
    # SPI_DEVICE = 0
    # mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    
    last_val = 0
    curr_val = 0
    
    while True:
        curr_val = mcp.read_adc(channel)

        # detect high
        print(curr_val)
        if curr_val>MID:
            curr_val = mcp.read_adc(channel)
            time.sleep(time_period/10)
            while True:
                curr_val = mcp.read_adc(channel)
                print(curr_val)
                # x = int(res[index])
                # index += 1
                if (curr_val < MID):
                    start = time.time()
                    print(start)
                    break
                    
            # neg edge detected, wait for the next bit
            
            break
    

    payload = ''  # Holds the message in bits
    table_string = ''  # Holds the table in bits
    string = '' # all the bits
    header = 0
    count = 8
    #start = time.time()
    # Main program loop.
    
    # read len of transmitted msg
    count = 16
    transmit_msg_len = 0
        
    while count>0:
        last_val = curr_val
        curr_val = mcp.read_adc(channel)
        curr_time = time.time()
        
        if(curr_val > MID and last_val<MID):
            # this means pos edge detected i.e 0->1
            # add 1 to the total bit string
            transmit_msg_len += (1<<(count-1))
            count -=1
            start = time.time()

            
            
        elif(((curr_val>MID and last_val>MID) or (curr_val<MID and last_val<MID))):
            #print('Time before getting in',time.time() - start)
            if((curr_time - start) > time_period*1.1):
                #print(time.time() - start)
                if(curr_val>MID):
                    transmit_msg_len += (1<<(count-1))
                else:
                    transmit_msg_len += (0<<(count-1))    
                #print('START',start)
                start = time.time()
                count -= 1
            
                
        elif(curr_val<MID and last_val>MID):
            # neg edge detected
            transmit_msg_len += (0<<(count-1))
            start = time.time()
            count -=1
            
    
    print('LEN', transmit_msg_len)
    
    count = transmit_msg_len
    while count>0:
        # The read_adc function will get the value of the specified channel (0-7).
        last_val = curr_val
        #curr_time = time.time()
        curr_val = mcp.read_adc(channel)
        curr_time = time.time()
        
        if(curr_val > MID and last_val<MID):
            # this means pos edge detected i.e 0->1
            # add 1 to the total bit string
            string +=str(1)
            start = time.time()
            print('String', string)
            print('pos edge 1\n')
            count -= 1
            
            
        elif(((curr_val>MID and last_val>MID) or (curr_val<MID and last_val<MID))):
            #print('Time before getting in',time.time() - start)
            if((curr_time - start) > time_period*1.1):
                #print(time.time() - start)
                if(curr_val>MID):
                    string += str(1)
                else:
                    string += str(0)    
                #print('START',start)
                start = time.time()
                print('String', string)
                print('consecutive 1 or 0\n')
                count -=1
                
            
                
            
                
        elif(curr_val<MID and last_val>MID):
            # neg edge detected
            string += str(0)
            start = time.time()
            print('String', string)
            
            print('neg edge 0\n')
            count -=1
        
        
    
    # the reception ends here
    
    f.write(string)
    f.close()

try:
    run()
except KeyboardInterrupt:
    pass
finally:
    # GPIO.cleanup()
    pass
