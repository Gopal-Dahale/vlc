def print_stats(duration, len_msg):
    print('Total bits send: ', len_msg * 8)
    print('Total time taken(s): ', duration)
    print('Datarate(bps): ', len_msg * 8 / (duration))


def add_header(payload, type_payload, len_payload):
    '''
    type: 0 for table, 1 for data
    len: 4 bits representing maximum of 15 bytes
    '''
    header = [type_payload, len_payload]
    return bytes(header) + payload


def fragment_bytes(msg_bytes, index, len_msg, max_bytes_processing=40):
    '''
    returns the fragment of bytes that can be send in one processing
    ex - total msg size is 100 bytes, then only 40 can be processed at once which 
    will be send in packets of 4 bytes
    '''
    if (len_msg - index > max_bytes_processing):
        return msg_bytes[index:index + max_bytes_processing]
    else:
        return msg_bytes[index:]


def prepare_packet(fragment, type_payload, index, max_payload=4):
    '''
    returns the packet with header and payload
    '''
    if (len(fragment) - index >= max_payload):
        len_payload = max_payload
    else:
        len_payload = len(fragment) - index
    return add_header(fragment[index:index + max_payload], type_payload,
                      len_payload)