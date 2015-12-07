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
	

class ClientDataWR:
		def __init__(self, DevID, DataNum, Addr_list, DataIn_list, Mask_list):
			self.DevID = DevID
			#self.Func = Func
			self.DataNum = DataNum
			self.Addr_list = Addr_list
			self.DataIn_list = DataIn_list
			self.Mask_list = Mask_list
			self.Header = 0x80
			self.FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DisWordRd':34, 
					'WordWt':49, 'DisWordWt':50}			
			self.DataOut = []
			self.u16DataOut_list = []
			self.u16ChkSum = 0
						
		def DisWordWt(self):
			
			DataOut.append(Header) 
			DataOut = DataOut + WordTo3Byte(D_ID)
			DataOut.append( (self.FuncCommTable[DisWordWt] & 0x7f) )
			DataOut = DataOut + WordTo3Byte(DataNum)
			for i in range(0,len(Addr_list)):
				DataOut =  DataOut + WordTo3Byte(Addr_list[i]) 
			for i in range(0,len(DataIn_list)):
				DataOut =  DataOut + WordTo3Byte(DataIn_list[i]) 
			for i in range(0,len(Mask_list)):
				DataOut =  DataOut + WordTo3Byte(Mask_list[i]) 
			for i in range(0,len(DataOut)):
				u16ChkSum = u16ChkSum + DataOut[i]
			u16ChkSum = u16ChkSum & 0xffff	
			DataOut = DataOut + WordTo3Byte(u16ChkSum)
	
			print(DataOut)
			return DataOut

def CopDiscWordWt(DevID, FuncCT, DataNum, Addr_list, DataIn_list):
	Header = 0x80
	DataOut = []
	u16ChkSum = 0
	DataOut.append(Header) 
	DataOut = DataOut + WordTo3Byte(DevID)
	DataOut.append( FuncCT )
	DataOut = DataOut + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut =  DataOut + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(DataIn_list)):
		DataOut =  DataOut + WordTo3Byte(DataIn_list[i]) 
	for i in range(0,len(DataOut)):
		u16ChkSum = u16ChkSum + DataOut[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut = DataOut + WordTo3Byte(u16ChkSum)
	return DataOut
	
def CopBitModify(DevID, FuncCT, DataNum, Addr_list, DataIn_list, Mask_list):
	Header = 0x80
	DataOut = []
	u16ChkSum = 0
	DataOut.append(Header) 
	DataOut = DataOut + WordTo3Byte(DevID)
	DataOut.append( FuncCT )
	DataOut = DataOut + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut =  DataOut + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(DataIn_list)):
		DataOut =  DataOut + WordTo3Byte(DataIn_list[i]) 
	for i in range(0,len(Mask_list)):
		DataOut =  DataOut + WordTo3Byte(Mask_list[i]) 
	for i in range(0,len(DataOut)):
		u16ChkSum = u16ChkSum + DataOut[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut = DataOut + WordTo3Byte(u16ChkSum)
	return DataOut		
			
def ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list):

	#CommTab_list = [0, 0, 17, 18, 33, 34, 49, 50]
	FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DiscWordRd':34, 
					'WordWt':49, 'DiscWordWt':50}

	if(Func == 'DiscWordWt'):
		print('Out:')
		print(CopDiscWordWt(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list))
	else:
		print('ERROR')
	return()
			
	
def Client485():
	DataOut = []
	u16DataOut_list = []
	u16ChkSum = 0
	#CommTab_list = [0, 0, 17, 18, 33, 34, 49, 50]
	FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DisWordRd':34, 
					'WordWt':49, 'DisWordWt':50}
	Header = 0x80	
	#D_ID = Deivce id
	D_ID = 0x01;
	#Func = Function ID
	#Func = 0x07
	Func = 'DisWordWt'
	#DataNum
	DataNum = 0x01
	#Addr
	Addr_list = [0x0]	#test
	#DataIn
	DataIn_list = [0x01]	#test
	#Mask
	Mask_list = [] #test
	
	#CommId = CommTab_list[Func]
	#DataOut = DataOut + list(Header) + list( WordTo3Byte(D_ID) )
	
	#add Header
	DataOut.append(Header) 
	#add ID
	DataOut = DataOut + WordTo3Byte(D_ID)
	#add Command Table (Func)
	#DataOut.append( (CommTab_list[Func] & 0x7f) )
	DataOut.append( (FuncCommTable[Func] & 0x7f) )
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
	for i in range(0,len(DataOut)):
		u16ChkSum = u16ChkSum + DataOut[i]
	#16bit Mask
	u16ChkSum = u16ChkSum & 0xffff	
	print (u16ChkSum)
	DataOut = DataOut + WordTo3Byte(u16ChkSum)
	
	
	#print ([hex(i) for i in DataOut])
	print(DataOut)
	return DataOut

def TestP0():
	print(0)
def TestP1():
	print(1)		
def TestP2():
	print(2)		
def TestPP(N):
	Ptable = {
				1:TestP0(),
				2:TestP1(),
				3:TestP2()
			}
	return Ptable[N]

	
if __name__ == '__main__':
    
	print ( WordTo3Byte(0x75f3) )
	#SerialWR([0x80,0x01,0x00,0x00,0x32,0x01,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x35,0x01,0x00])
	print(Client485())
	ClientOp(1, 'DiscWordWt', 1, [0x00], [0x01],[])
	
	#ClientDataWR(0x01, 1,  [0x00], [0x01], [])
	#print(ClientDataWR.DisWordWt)
	'''
	DWR = ClientDataWR
	DWR.DevID = 1
	DWR.DataNum = 1
	DWR.Addr_list = [0x00]
	DWR.DataIn_list = [0x01]
	DWR.Mask_list = []
	print(DWR.DisWordWt)'''
	#SerialWR(Client485())
	#SerialWR ([128, 1, 0, 0, 50, 1, 0, 0, 0, 0, 0, 1, 0, 0, 53, 1, 0])