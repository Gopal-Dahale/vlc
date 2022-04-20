from audioop import reverse
import pyae

# Example for encoding a simple text message using the PyAE module.
# This example returns the floating-point value in addition to its binary code that encodes the message.

frequency_table = {"a": 10, "b": 10, "c": 10}

AE = pyae.ArithmeticEncoding(frequency_table=frequency_table, save_stages=False)

original_msg = "abcabcabcabcabcabcabcabcabcabc"
print("Original Message: {msg}".format(msg=original_msg))

# Encode the message
encoded_msg, encoder, interval_min_value, interval_max_value = AE.encode(
    msg=original_msg, probability_table=AE.probability_table)
print("Encoded Message: {msg}".format(msg=encoded_msg))

# Get the binary code out of the floating-point value
binary_code, encoder_binary = AE.encode_binary(
    float_interval_min=interval_min_value,
    float_interval_max=interval_max_value)
print("The binary code is: {binary_code}".format(binary_code=binary_code))

print(binary_code[2:])

print("bin2float", pyae.bin2float(binary_code))

# Decode the message
decoded_msg, decoder = AE.decode(encoded_msg=pyae.bin2float(binary_code),
                                 msg_length=len(original_msg),
                                 probability_table=AE.probability_table)
decoded_msg = "".join(decoded_msg)
print("Decoded Message: {msg}".format(msg=decoded_msg))

print("Message Decoded Successfully? {result}".format(
    result=original_msg == decoded_msg))
