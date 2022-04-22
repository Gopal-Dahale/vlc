import time
import RPi.GPIO as GPIO

# Constants
time_period = 0.05  # seconds
threshold = 260
data_pin = 3


def print_stats(duration, len_msg):
    print('Total bits send: ', len_msg * 8)
    print('Total time taken(s): ', duration)
    print('Datarate(bps): ', len_msg * 8 / (duration))


def add_header(payload, type_payload, len_payload):
    '''
    type: 0 for table, 1 for data
    len: 4 bits representing maximum of 15 bytes
    '''
    # print('payload: ', payload)
    # print('type_payload: ', type_payload)
    # print('len_payload: ', len_payload)
    # print('bin type_payload', bin(type_payload)[2:])
    # print('bin len_payload', bin(len_payload)[2:].zfill(7))
    header = bin(type_payload)[2:] + bin(len_payload)[2:].zfill(7)
    # print('header', header)
    # print('len header', len(header))
    packet = header + payload
    # print('packet', packet)
    # print('len packet', len(packet))
    return packet


def fragment_bits(msg_bits, index, len_msg, max_bits_processing=80):
    '''
    returns the fragment of bits that can be send in one processing
    ex - total msg size is 100 bits, then only 40 can be processed at once which 
    will be send in packets of 4 bits
    '''
    if (len_msg - index > max_bits_processing):
        return msg_bits[index:index + max_bits_processing]
    else:
        return msg_bits[index:]


def prepare_packet(fragment, type_payload, index, max_payload=32):
    '''
    returns the packet with header and payload
    max_payload = 32 bits
    '''
    assert (max_payload < 128, 'max_payload should be less than 128')
    if (len(fragment) - index >= max_payload):
        len_payload = max_payload
    else:
        len_payload = len(fragment) - index
    return add_header(fragment[index:index + max_payload], type_payload,
                      len_payload)


def transmit_byte(byte):
    # bit_stream = byte
    # print(bit_stream)
    i = 7
    # print("BYTE", byte)

    while (i >= 0):
        print(1 if (byte & (1 << i)) else 0, end = '')

        ################# TEST START ######################
        # file = open('transmit_out.txt', 'a')
        # file.write(str(1 if (byte & (1 << i)) else 0))
        # file.close()
        ################# TEST END ######################

        GPIO.output(data_pin, (byte & (1 << i)))
        # GPIO.output(data_pin, 1)
        time.sleep(time_period)
        i -= 1
    # print('\n')