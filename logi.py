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
			
			#Wire Block
			print ("Wire is Start") 
			#ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x00\x00\x00\x01\x00\x00\x35\x01\x00') 
			ser.write(DataWr[:])
			#Wire Block End
			
			'''
			#Read Block
			i = 0

			print ("Read is Start")  
			tStart = time.time()
			while( (1 > ( time.time() - tStart )) ):
					if ser2.inWaiting():
							print ( ser2.read(ser2.inWaiting()) )
					i = i + 1
					print (   time.time() - tStart )
					print ( i )
			#Read Block End
			'''
	print ("Wire&Read is Over")     

	ser.close()
	return 

	
	
def Client485():
	DataOut = []
	u16DataOut_list = []
	u16ChkSum = 0

	CommTab_list = [0, 0, 17, 18, 33, 34, 49, 50]
	Header = 0x80	
	#D_ID = Deivce id
	D_ID = 0x00;
	#Func = Function ID , 00=Intl
	Func = 0x00
	#DataNum
	DataNum = 0x00
	#Addr
	Addr_list = [0xff01,0xffff]	#test
	#DataIn
	DataIn_list = [0xff01,0xf355]	#test
	#Mask
	Mask_list = [0xff01, 0x5238] #test
	
	#CommId = CommTab_list[Func]
	#DataOut = DataOut + list(Header) + list( WordTo3Byte(D_ID) )
	
	#add Header
	DataOut.append(Header) 
	#add ID
	DataOut = DataOut + WordTo3Byte(D_ID)
	#add Command Table (Func)
	DataOut.append( (CommTab_list[Func] & 0x7f) )
	#add DataNum
	DataOut = DataOut + WordTo3Byte(DataNum)
	#add Addr_list
	for i in range(0,len(Addr_list)):
		DataOut =  DataOut + WordTo3Byte(Addr_list[i]) 
	#add DataIn
	for i in range(0,len(DataIn_list)):
		DataOut =  DataOut + WordTo3Byte(DataIn_list[i]) 
	#add Mask_list
	for i in range(0,len(Mask_list)):
		DataOut =  DataOut + WordTo3Byte(Mask_list[i]) 
	
	print( DataOut )
	print ([hex(i) for i in DataOut])
	
	#add ChkSum
	#DataOut to U16
	#u8list to u16list
	for i in range(0,len(DataOut)//2):
		u16ChkSum = u16ChkSum + ((DataOut[i*2]<<8)+DataOut[(i*2)+1])
	#16bit Mask
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut = DataOut + WordTo3Byte(u16ChkSum)
	
	print ([hex(i) for i in DataOut])
	#for i in range(0,len(DataOut)):
	#	u16DataOut_list.append( struct.pack('H', (DataOut[i]*0x100)+DataOut[i+1]]  ) 
		
	#u16test= bytearray(DataOut)	
	
	return DataOut

	
if __name__ == '__main__':
    
	print ( WordTo3Byte(0x75f3) )
	#SerialWR([0x80,0x01,0x00,0x00,0x32,0x01,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x35,0x01,0x00])
	Client485()