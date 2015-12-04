import struct



def WordTo3Byte():

    u16word = 0x7356
    
    
    u8Byte = [0x00,0x00,0x00]

    
    u16Data = struct.pack("H", u16word)
   
    # s to 2 B (byte)element
    u16wByte0, u16wByte1 =  struct.unpack("2B", u16Data)
    #8bL, 8bH = 16w

    #move to u8B[2]    ok
    u8Byte[2] = u16wByte1 >> 6

    #move to u8B[0]    ok
    u8Byte[0] = u16wByte0 & 0x7f

            
    #move to u8B[1]
            
    u16word = ( u16word << 1) & 0x7f00
    u16Data = struct.pack("H", u16word)
    print ( u16Data )
    u16wByte0, u16wByte1 =  struct.unpack("2B", u16Data)
    u8Byte[1] = u16wByte1
    
 
    print (u8Byte[2])
    print (u8Byte[1])
    print (hex(u8Byte[2]) )  
    print (hex(u8Byte[1]) )
    print (hex(u8Byte[0]) )
    #bin hex


if __name__ == '__main__':
    WordTo3Byte()
