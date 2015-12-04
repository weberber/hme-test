import struct



def WordTo3Byte():

    u16word = 0xf0ff
    
    u8Byte = [0x00,0x00,0x00]

    
    u16Data = struct.pack("H", u16word)
   
    u8Byte0, u8Byte1 =  struct.unpack("2B", u16Data)
    # s to 2 B (byte)element

    print (u8Byte0)
    print (u8Byte1)
    print (1)


if __name__ == '__main__':
    WordTo3Byte()
