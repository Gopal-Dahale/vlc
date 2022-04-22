import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from utils import threshold, time_period

data_pin = 12
GPIO.setup(data_pin, GPIO.OUT, initial=0)

# Software SPI configuration:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
channel = 0
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)



def run():
    print('Reading MCP3008 values, press Ctrl-C to quit...')

    ################# TEST START ######################
    file = open('transmit_out.txt', 'r')
    res = file.read()
    print(res)
    index = 0
    ################# TEST END ######################
    x = 0

    # Recieve the message

    # Recieve HIGH for some period of time
    # and then recieve LOW for the reciever
    # to detect the start of the message
    while True:
        # x = mcp.read_adc(channel)
        x = int(res[index])
        index += 1

        # detect high
        if x > threshold:
            # x = mcp.read_adc(channel)
            print('positive detected')

            # loop until low detected
            while True:
                # x = mcp.read_adc(channel)
                x = int(res[index])
                index += 1
                if (x < threshold):
                    break

            # 0 detected after detecting 1
            # wait for 1 T and sample
            print('neg edge detected')
            time.sleep(time_period * 1)
            index += 7
            break

    # Recieve the message
    count = 8
    byte = 0
    string = ''  # Holds the message in bits
    table_string = ''  # Holds the table in bits
    while True:
        x = mcp.read_adc(channel)
        # x = int(res[index])
        # print(x, end='')
        # index += 1

        x = (1 if x > threshold else 0)
        byte += (x << (count - 1))
        count -= 1

        # A byte is recieved
        if (count == 0):
            # print('\n')
            # print('byte recieved')
            count = 8
            # print(bin(byte)[2:].zfill(8))

            # Since this is the first byte of a packet
            # it contains header which has info about the
            # packet
            type_payload = (byte >> 7)
            len_payload = (byte & 0x7F)
            # print('type payload', type_payload)
            # print('len_payload', bin(len_payload)[2:].zfill(7))
            # print("LEN PAYLOAD", len_payload)

            # Ideally the length of payload should be 32 bits
            # # i.e.length of payload should be 32
            if (len_payload == 32):
                # We need to recieve more 32 bits in order to fully recieve the packet
                remaining_bits = 32
                while remaining_bits:
                    x = mcp.read_adc(channel)
                    # x = int(res[index])
                    # print(x, end='')
                    # index += 1
                    x = (1 if x > threshold else 0)
                    if type_payload:
                        string += str(x)
                    else:
                        table_string += str(x)
                    remaining_bits -= 1
                    time.sleep(time_period)

            elif (len_payload < 32):
                # This case arises in the terminal stage of the fragment
                max_num_bytes = len_payload // 8  # Maximum number of proper bytes we can capture
                remaining_bits = max_num_bytes * 8
                special_bits = len_payload - remaining_bits
                count = 8

                while remaining_bits:
                    x = mcp.read_adc(channel)
                    # x = int(res[index])
                    # print(x, end='')
                    # index += 1
                    x = (1 if x > threshold else 0)
                    if type_payload:
                        string += str(x)
                    else:
                        table_string += str(x)
                    remaining_bits -= 1
                    time.sleep(time_period)

                if special_bits:
                    temp = ''
                    while count:
                        x = mcp.read_adc(channel)
                        # x = int(res[index])
                        # print(x, end='')
                        # index += 1
                        x = (1 if x > threshold else 0)
                        temp += str(x)
                        count -= 1
                        time.sleep(time_period)

                    if type_payload:
                        string += temp[-special_bits:]
                    else:
                        table_string += temp[-special_bits:]

            byte = 0

        time.sleep(time_period)
        # print("TABLE STRING", table_string)
        # print("STRING", string)

    print(str1)


try:
    run()
except KeyboardInterrupt:
    pass
finally:
    pass
