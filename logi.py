import struct
import serial
import time


def WordTo3Byte(u16word):

#    u16word = 0x7356
     
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
    u16wByte0, u16wByte1 =  struct.unpack("2B", u16Data)
    u8Byte[1] = u16wByte1
    
	
    #print (hex(u8Byte[2]) )  
    #print (hex(u8Byte[1]) )
    #print (hex(u8Byte[0]) )
	
    #bin hex
	
    return u8Byte

def SerialWR(DataWr):
	
	ser = serial.Serial()
	#ser.port = "/dev/ttyUSB0"
	ser.port = "COM15"
	ser.baudrate = 115200
	ser.timeout = None
	#not stop
	
	ser.open()
	
	if ser.isOpen():
			print ("USB0 is OK")
			print ("Wire is Start") 
			#ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x00\x00\x00\x01\x00\x00\x35\x01\x00') 
			ser.write(DataWr[:])
			
			'''
			i = 0

			print ("Read is Start")  
			tStart = time.time()
			while( (1 > ( time.time() - tStart )) ):
					if ser2.inWaiting():
							print ( ser2.read(ser2.inWaiting()) )
					i = i + 1
					print (   time.time() - tStart )
					print ( i )
			'''
	print ("Wire&Read is Over")     

	ser.close()
	return 
	
	
def Client485():

	Header = 0x80	
	#D_ID = Deivce id
	D_ID = 0x00;
	#Func = Function ID , 00=Intl
	Func = 0x00
	#DataNum
	DataNum = 0x00
	#Addr
	Addr = 0x00
	#DataIn
	DataIn = 0x00
	#Mask
	Mask = 0x00
	
	
if __name__ == '__main__':
    
	print ( WordTo3Byte(0x75f3) )
	SerialWR([0x80,0x01,0x00,0x00,0x32,0x01,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x35,0x01,0x00])
