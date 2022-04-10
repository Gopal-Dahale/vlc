import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#data_pin = 12
#GPIO.setup(data_pin, GPIO.OUT, initial=0)

# Software SPI configuration:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
channel = 0
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


time_period = 0.150  # seconds
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
        #print(x)
        # detect high
        if x > threshold:
            x = mcp.read_adc(channel)
            #print(x)
            print('positive detected')
            
            # loop until low detected
            while True:
                x = mcp.read_adc(channel)
                
                if(x<threshold):
                    break
            
            #0 detected after detecting 1
            #wait for 1 T and sample
            print('neg edge detected')
            time.sleep(time_period*1)
           
            break

    # Recieve the message
    count = 0
    byte = 0
    str1 = ''
    i = 0
    while True:
        start = time.time()
        x = mcp.read_adc(channel)
        x = (1 if x>threshold else 0)
        #print(x)
        byte += (x<<count)
        count+=1
        i+=1
        
        if(count == 8):
            count = 0
            str1 += chr(byte)
            print(chr(byte))
            byte = 0
            
        time.sleep(time_period)
        
        #end = time.time()
        #print(end-start)
        
    
    print(str1)

try:
    run()
except KeyboardInterrupt:
    pass
finally:
    pass
    
