import time
from utils import fragment_bits, prepare_packet, transmit_byte


def run_length_encode(sequence):
    encoded_string = ""
    i = 0
    while (i <= len(sequence) - 1):
        count = 1
        ch = sequence[i]
        j = i
        while (j < len(sequence) - 1):
            '''if the character at the current index is the same as the character at the next index. If the characters are the same, the count is incremented to 1'''
            if (sequence[j] == sequence[j + 1]):
                count = count + 1
                j = j + 1
            else:
                break
        '''the count and the character is concatenated to the encoded string'''
        encoded_string = encoded_string + str(count) + ch
        i = j + 1
    return encoded_string


def run_length_decode(sequence):
    decode = ''
    count = ''
    for char in sequence:
        # If the character is numerical...
        if char.isdigit():
            # ...append it to our count
            count += char
        else:
            # Otherwise we've seen a non-numerical
            # character and need to expand it for
            # the decoding
            decode += char * int(count)
            count = ''
    return decode


def run_length_transmit(encoded_msg, max_payload=32, max_bits_processing=64):
    len_encoded_msg = len(encoded_msg)
    index = 0
    start = time.time()
    print('Starting transmission\n')
    while (index < len_encoded_msg):
        fragment = fragment_bits(encoded_msg, index, len_encoded_msg,
                                 max_bits_processing)
        print("FRAGMENT", fragment)
        print("LEN FRAGMENT", len(fragment))
        index += max_bits_processing
        i = 0
        while (i < len(fragment)):
            print('Sending packet')
            packet = prepare_packet(fragment, 1, i, max_payload)
            print("PACKET", packet)
            len_packet = len(packet)
            for k in range(0, len_packet, 8):
                if (k + 8 < len_packet):
                    byte = int(packet[k:k + 8], 2)
                else:
                    byte = int(packet[k:], 2)
                transmit_byte(byte)
            i += max_payload

    end = time.time()
    return end - start


# def main():
#     print("Run Length Encoding and Decoding")
#     print("==============================================")
#     h = int(
#         input(
#             "Enter 1 if you want to enter in command window, 2 if you are using some file:"
#         ))
#     if h == 1:
#         string = input("Enter the string you want to compress:")
#     elif h == 2:
#         file = input("Enter the filename:")
#         with open(file, 'r') as f:
#             string = f.read()
#     else:
#         print("You entered invalid input")
#     encoded = run_length_encode(string)
#     print("Encoded String: " + (encoded))
#     decoded = run_length_decode(encoded)

#     print("Decoded String: " + decoded)
#     print('check', decoded == string)

# if __name__ == "__main__":
#     main()