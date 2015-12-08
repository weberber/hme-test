import struct
import serial
import time

def WordTo3Byte(u16word):
    u8Byte = [0x00,0x00,0x00]
    u16Data = struct.pack("H", u16word)
   
    # s to 2B (byte)element
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
    return u8Byte
	
def u3ByteToWord(u3Byte):
	return(u3Byte[0] + ((u3Byte[1]<<7)&0xff) + (((u3Byte[1]>>1) + (u3Byte[2]<<6))* 0x100))
	

def SerialWR(DevID, DataWr_list, Func, DataNum):
	u16ReData_list = []
	
	ser = serial.Serial()
	#ser.port = "/dev/ttyUSB0"
	ser.port = "COM18"
	ser.baudrate = 115200
	ser.timeout = None
	#not stop
	FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DiscWordRd':34, 
					'WordWt':49, 'DiscWordWt':50}
	
	ser.open()
	
	if ser.isOpen():
	
			print (ser.port, "is OK")
			
			#Wire Block
			print ("Wire is Start") 
			#ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x00\x00\x00\x01\x00\x00\x35\x01\x00') 
			ser.write(DataWr_list[:])
			#Wire Block End
			
			
			#Read Block
			DataRd_list = []
			RdBytesLen = 0
			RdBytesLenSum = 0 
			RdError_list = []
			RdTimeOut = False
			if(Func == 'WordRd' or Func == 'DiscWordRd'):
				ResponseNum = (DataNum * 3) + 8
			else:
				ResponseNum = 8
				
			print ("Read is Start")  			
			tStart = time.time()
			while(RdTimeOut != True and RdBytesLenSum < ResponseNum):				
				if ser.inWaiting():
					RdBytesLen = ser.inWaiting()
					#DataRd_list = All Read Datas
					DataRd=ser.read(RdBytesLen)
					#Bytes to U8list
					DataRd_list += (struct.unpack('%dB'%(RdBytesLen), DataRd))
					RdBytesLenSum += RdBytesLen
					print ('Time=', (time.time() - tStart)*1000,'ms')	
					#print (ResponseNum)		
				#Time Out	
				if(0.05 < time.time()-tStart):	
					RdTimeOut = True
					RdError_list.append('TimeOutErr')	
			print('DataRd_list = ', DataRd_list)
			#Read Over
			
			#Check RespNumErr
			if(len(DataRd_list) != ResponseNum):
				RdError_list.append('RespNumErr')
				print('RespNumErr')
				print(len(DataRd_list))
				# !!
				DataRd_list = []
				#return()
				
			#Check ChkSumErr
			RespData_list = DataRd_list[0:len(DataRd_list)-3]
			ChkSum_list = DataRd_list[len(DataRd_list)-3:len(DataRd_list)]
			u16ReChkSum = sum(RespData_list) & 0xffff
			u8ReChkSum_list = WordTo3Byte(u16ReChkSum)			
			#print('ReD_L=',RespData_list)
			#print('Chk_L=',ChkSum_list)
			#print('16ReChk=', u16ReChkSum)		
			#print( 'ReChk_L=', u8ReChkSum_list)			
			if(ChkSum_list != u8ReChkSum_list):
				RdError_list.append('ChkSumErr')
				# !!
				DataRd_list = []
				
			#Check FormatErr
			#RespData_list = DataRd_list[0:len(DataRd_list)-3]
			HeadIdComm_list = RespData_list[0:5]
			#print('HIC_L=',HeadIdComm_list)					
			if(HeadIdComm_list[0] != 0xc0 or HeadIdComm_list[1:4] != WordTo3Byte(DevID) or FuncCommTable[Func] != HeadIdComm_list[4] ) :
				RdError_list.append('FormatErr')
				# !!
				DataRd_list = []
				
			#RAW to Data	
			Re3BDataOut_list = []
			BoolChk = 0
			print('DR_L=',DataRd_list)			
			ReData_list = DataRd_list[5:len(DataRd_list)-3]		
			print('RD_L=',ReData_list)
			print(DataRd_list)		
			for i in range(0, (len(ReData_list)//3)):
				Re3BDataOut_list.append(ReData_list[i*3:i*3+3] )
			print('R3B_L=', Re3BDataOut_list)
			#Chack FormatErr
			if(Func == 'BitModify')	:
				u16ReData_list = []
				#Read Block End
			else:
				for i in range(0, len(Re3BDataOut_list)):
					BoolChk +=  (Re3BDataOut_list[i][0] & 0x80)
					BoolChk +=  (Re3BDataOut_list[i][1] & 0x80)
					BoolChk +=  (Re3BDataOut_list[i][2] & 0xfc)
				if(BoolChk == 0):
					#Ok
					for i in range(0, len(Re3BDataOut_list)):
						u16ReData_list.append(u3ByteToWord(Re3BDataOut_list[i]) )
					print('Data = ',u16ReData_list)
					print ('Data = ', [hex(i) for i in u16ReData_list])
				else:
					RdError_list.append('FormatErr')
					#!!
					DataRd_list = []
			#Read Block End
						
	print ("Wire&Read is Over")
	if(len(RdError_list)):
		print (RdError_list)

	ser.close()
	return (u16ReData_list)
	

'''
ClientOp()
	|---CopDiscWordWt
	|---CopBitModify
	|---CopBitInv
	|---CopWordRd
	|---CopWordWt
'''
def CopDiscWordWt(DevID, FuncCT, DataNum, Addr_list, DataIn_list):
	Header = 0x80
	DataOut_list = []
	u16ChkSum = 0
	DataOut_list.append(Header) 
	DataOut_list = DataOut_list + WordTo3Byte(DevID)
	DataOut_list.append( FuncCT )
	DataOut_list = DataOut_list + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(DataIn_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(DataIn_list[i]) 
	for i in range(0,len(DataOut_list)):
		u16ChkSum = u16ChkSum + DataOut_list[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut_list = DataOut_list + WordTo3Byte(u16ChkSum)
	return DataOut_list
	
def CopBitModify(DevID, FuncCT, DataNum, Addr_list, DataIn_list, Mask_list):
	Header = 0x80
	DataOut_list = []
	u16ChkSum = 0
	DataOut_list.append(Header) 
	DataOut_list = DataOut_list + WordTo3Byte(DevID)
	DataOut_list.append( FuncCT )
	DataOut_list = DataOut_list + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(DataIn_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(DataIn_list[i]) 
	for i in range(0,len(Mask_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Mask_list[i]) 
	for i in range(0,len(DataOut_list)):
		u16ChkSum = u16ChkSum + DataOut_list[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut_list = DataOut_list + WordTo3Byte(u16ChkSum)
	return DataOut_list		
	
def CopBitInv(DevID, FuncCT, DataNum, Addr_list, Mask_list):
	Header = 0x80
	DataOut_list = []
	u16ChkSum = 0
	DataOut_list.append(Header) 
	DataOut_list = DataOut_list + WordTo3Byte(DevID)
	DataOut_list.append( FuncCT )
	DataOut_list = DataOut_list + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(Mask_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Mask_list[i]) 
	for i in range(0,len(DataOut_list)):
		u16ChkSum = u16ChkSum + DataOut_list[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut_list = DataOut_list + WordTo3Byte(u16ChkSum)
	return DataOut_list		
	
def CopWordRd(DevID, FuncCT, DataNum, Addr_list):
	Header = 0x80
	DataOut_list = []
	u16ChkSum = 0
	DataOut_list.append(Header) 
	DataOut_list = DataOut_list + WordTo3Byte(DevID)
	DataOut_list.append( FuncCT )
	DataOut_list = DataOut_list + WordTo3Byte(DataNum)
	DataOut_list =  DataOut_list + WordTo3Byte(Addr_list[0]) 
	for i in range(0,len(DataOut_list)):
		u16ChkSum = u16ChkSum + DataOut_list[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut_list = DataOut_list + WordTo3Byte(u16ChkSum)
	return DataOut_list		

def CopWordWt(DevID, FuncCT, DataNum, Addr_list, DataIn_list):

	Header = 0x80
	DataOut_list = []
	u16ChkSum = 0
	DataOut_list.append(Header) 
	DataOut_list = DataOut_list + WordTo3Byte(DevID)
	DataOut_list.append( FuncCT )
	DataOut_list = DataOut_list + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(DataIn_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(DataIn_list[i]) 
	for i in range(0,len(DataOut_list)):
		u16ChkSum = u16ChkSum + DataOut_list[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut_list = DataOut_list + WordTo3Byte(u16ChkSum)
	return DataOut_list	

def CopDiscWordRd(DevID, FuncCT, DataNum, Addr_list):
	Header = 0x80
	DataOut_list = []
	u16ChkSum = 0
	DataOut_list.append(Header) 
	DataOut_list = DataOut_list + WordTo3Byte(DevID)
	DataOut_list.append( FuncCT )
	DataOut_list = DataOut_list + WordTo3Byte(DataNum)
	for i in range(0,len(Addr_list)):
		DataOut_list =  DataOut_list + WordTo3Byte(Addr_list[i]) 
	for i in range(0,len(DataOut_list)):
		u16ChkSum = u16ChkSum + DataOut_list[i]
	u16ChkSum = u16ChkSum & 0xffff	
	DataOut_list = DataOut_list + WordTo3Byte(u16ChkSum)
	return DataOut_list		
	
	
def ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list):

	#CommTab_list = [0, 0, 17, 18, 33, 34, 49, 50]
	FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DiscWordRd':34, 
					'WordWt':49, 'DiscWordWt':50}

	if(Func == 'DiscWordWt'):
		return(CopDiscWordWt(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list))
	elif(Func == 'BitModify'):
		return(CopBitModify(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list, Mask_list))
	elif(Func == 'BitInv'):
		return(CopBitInv(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, Mask_list))
	elif(Func == 'WordRd'):
		return(CopWordRd(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list))
	elif(Func == 'DiscWordRd'):
		return(CopDiscWordRd(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list))
	elif(Func == 'WordWt'):
		return(CopWordWt(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list))
	else:
		print('ERROR')
		return()

def TestPj():
	DevID = 0x01
	Func = 'DiscWordWt'
	DataNum = 2
	#Test Addr Range = 200~1000
	#ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list)
	DW = ClientOp(DevID, Func, DataNum, [355, 358], [0xffff,0xeeee],[])
	SerialWR(DevID, DW, Func, DataNum)
	
def TestPj2():
	DevID = 0x01
	Func = 'DiscWordRd'
	DataNum = 2
	#Test Addr Range = 200~1000
	#ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list)
	DW = ClientOp(DevID, Func, DataNum, [355, 358],[],[])
	print(SerialWR(DevID, DW, Func, DataNum))
	
if __name__ == '__main__':
    
	TestPj()
	TestPj2()

	
