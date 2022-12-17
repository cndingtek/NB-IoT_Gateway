import struct
class utility(object):

    @staticmethod
    def hex_to_ascii(h):
        list_s = []
        for i in range(0, len(h), 2):
            list_s.append(chr(int(h[i:i + 2], 16)))
        return ''.join(list_s)

    @staticmethod
    def ascii_to_hex(s):
        list_h = []
        for c in s:
            list_h.append(str(hex(ord(c))[2:]))
        return ''.join(list_h)


    # Func: convert hex data to float in IEEE754 format
    # Param: data_in: input data in hex#
    # return: outdata in float
    @staticmethod
    def IEEE754_Hex_To_Float(data_in):
        # change order
        # print("data_in is "+data_in)
        data_first = int("0x" + data_in, 16)
        # print("data_first 1 is " + str(data_first))
        data_middle = struct.pack("q", data_first)
        # print("data_middle 2 is " + str(data_middle))
        data_out = struct.unpack(">f", data_middle[0:4])[0]
        return data_out


    # Func: IEEE754->hex, big endian
    # Param: data_in, float data
    # Return: hex string
    @staticmethod
    def IEEE754_Float_To_Hex(data_in):
        # change order
        data_temp = hex(struct.unpack("l", struct.pack(">f", data_in))[0])
        data_out = data_temp[2:].rjust(8, '0').upper()
        return data_out
