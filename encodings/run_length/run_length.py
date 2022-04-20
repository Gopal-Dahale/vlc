from collections import OrderedDict
import re


def run_length_encode(sequence):
    dict = OrderedDict.fromkeys(sequence, 0)
    for ch in sequence:
        dict[ch] += 1
    output = ''
    for key, value in dict.items():
        output = output + key + str(value)
    return output


def run_length_decode(sequence):
    res = ""
    for (char, num) in re.findall(r'([a-z])([0-9]+)', sequence):
        res += (char * int(num))
    return res


def formatOutput(sequence):
    result = []
    for item in sequence:
        if (item[1] == 1):
            result.append(item[0])
        else:
            result.append(str(item[1]) + item[0])
    return "".join(result)


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