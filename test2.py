#-*- coding: utf-8 -*-

import struct
import serial
import time

def WordTo3Byte(u16word):
	#用於將1Word資料編碼為3Byte
	
	#u8Byte:用於存放轉好的資料,元素=Bytet,長度=3
    u8Byte = [0x00,0x00,0x00]

	
    u16Data = struct.pack("H", u16word)
    u16wByte0, u16wByte1 =  struct.unpack("2B", u16Data)

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
	#將經編碼之3Byte資料解碼為1Word
	return(u3Byte[0] + ((u3Byte[1]<<7)&0xff) + (((u3Byte[1]>>1) + (u3Byte[2]<<6))* 0x100))
	
def WordListToAdd3ByteList(WordDatat, Data_list):
	#用於將WordTypeList編碼為3Byte,並加入3ByteTypeList中
	for i in range(0,len(WordDatat)):
		Data_list =  Data_list + WordTo3Byte(WordDatat[i]) 
	return(Data_list)

def SerialWR(DevID, DataWr_list, Func, DataNum, RepeatNum):
	#將經編碼之資料由串列埠寫出,並接收與驗證回傳之資料後輸出
	#DevID = 裝置ID, DataWr_list = 欲寫出之資料 ,Func = 記憶體操作
	#DataNum = 欲寫出資料之長度(Word), RepeatNum = 重傳次數

	#u16ReData_list:存放回傳資料
	u16ReData_list = []

	ser = serial.Serial()
	#ser.port = "/dev/ttyUSB0"
	ser.port = "COM18"
	ser.baudrate = 115200
	#無timeout, 沒有接收到"足夠"資料時不會由COM Port停止等待
	ser.timeout = None

	FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DiscWordRd':34, 
				'WordWt':49, 'DiscWordWt':50}
	#致能COM Port
	ser.open()
	
	if ser.isOpen():
		#若COM Port 正常啟動
		print (ser.port, "is OK")
		
		#寫出資料
		ser.write(DataWr_list[:])
			
		#以下為讀入資料之程式區塊
		#DataRd_list:接收由串列埠回傳之資料
		DataRd_list = []
		#RdBytesLen:當前串列埠接收緩衝區內的資料(Byte)長度
		RdBytesLen = 0
		#RdBytesLenSum:本次已接收資料數
		RdBytesLenSum = 0 
		#RdError_list:錯誤訊息
		RdError_list = []
		#RdTimeOut:TimeOut旗標
		RdTimeOut = False
		
		#設定不同操作所應獲得之回傳資料長度
		if(Func == 'WordRd' or Func == 'DiscWordRd'):
			ResponseNum = (DataNum * 3) + 8
		else:
			ResponseNum = 8
			
		print ("Read is Start") 
		
		#開始從串列埠接收資料,自訂TimeOut迴圈
		tStart = time.time()
		#若接收時間大於50ms 或 接收資料長度<=預定接收長度
		while(RdTimeOut != True and RdBytesLenSum < ResponseNum):				
			if ser.inWaiting():
				#串列緩衝區內有資料, 取得資料長度並讀取
				RdBytesLen = ser.inWaiting()
				DataRd=ser.read(RdBytesLen)
				#Bytes to U8list
				DataRd_list += (struct.unpack('%dB'%(RdBytesLen), DataRd))
				RdBytesLenSum += RdBytesLen
				print ('Time=', (time.time() - tStart)*1000,'ms')	
				#print ('ResponseNum=', ResponseNum)		
			#Time Out	
			if(0.05 < time.time()-tStart):	
				RdTimeOut = True
				RdError_list.append('TimeOutErr')	
		print('DataRd_list = ', DataRd_list)
		#結束接收程序
		
		#開始驗證資料正確性
		#Check RespNumErr
		if(len(DataRd_list) != ResponseNum):
			RdError_list.append('RespNumErr')
			print('RespNumErr')
			print('RespNum=', ResponseNum,' DataRd_LNum=', len(DataRd_list))
			# !!
			DataRd_list = []
			#錯誤即結束
			return()
			
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
			#錯誤即結束
			return()
			
		#Check FormatErr
		HeadIdComm_list = RespData_list[0:5]
		#print('HIC_L=',HeadIdComm_list)					
		if(HeadIdComm_list[0] != 0xc0 or HeadIdComm_list[1:4] != WordTo3Byte(DevID) or FuncCommTable[Func] != HeadIdComm_list[4]):
			RdError_list.append('FormatErr')
			# !!
			DataRd_list = []
			#錯誤即結束
			return()
			
		#將原始接接收資料解碼( 3Byte to 1Word )	
		Re3BDataOut_list = []
		BoolChk = 0
		#print('DR_L=',DataRd_list)			
		ReData_list = DataRd_list[5:len(DataRd_list)-3]		
		#print('RD_L=',ReData_list)
		#print(DataRd_list)		
		for i in range(0, (len(ReData_list)//3)):
			Re3BDataOut_list.append(ReData_list[i*3:i*3+3] )
		print('R3B_L=', Re3BDataOut_list)
		#Chack FormatErr
		if(Func == 'BitModify')	:
			#不需檢查回傳
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
				#毒入資料驗證完成, u16ReData_list = 讀入資料
				print('Data = ',u16ReData_list)
				print ('Data = ', [hex(i) for i in u16ReData_list])
			else:
				RdError_list.append('FormatErr')
				#!!
				DataRd_list = []
		#以上為讀入資料之程式區塊
						
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
	
	
def ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list, RepeatNum):
	#用於進行通訊,讀寫操作燈具裝置之記憶體
	#DevID = 裝置ID, Func = 記憶體操作方式, DataNum = 資料長度(Word)
	#Addr_list = 欲操作之(燈具)記憶體位址, Mask_list = 位元操作遮罩, RepeatNum = 重傳次數上限
	
	#Func:{'Inital':, 'Close':, 'BitModify':寫入特定位元, 'BitInv':翻轉特定位元, 'WordRd':讀取連續記憶體位置,
	#	 'DiscWordRd':讀取非連續記憶體位置, 'WordWt':寫入連續記憶體位置, 'DiscWordWt':寫入非連續記憶體位置}
	
	#要寫入串列通訊的資料
	u16DataWt_list = []
	
	FuncCommTable = {'Inital':0, 'Close':0, 'BitModify':17, 'BitInv':18, 'WordRd':33, 'DiscWordRd':34, 
					'WordWt':49, 'DiscWordWt':50}

	if(Func == 'DiscWordWt'):
		u16DataWt_list = CopDiscWordWt(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list)
	elif(Func == 'BitModify'):
		u16DataWt_list = CopBitModify(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list, Mask_list)
	elif(Func == 'BitInv'):
		u16DataWt_list = CopBitInv(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, Mask_list)
	elif(Func == 'WordRd'):
		u16DataWt_list = CopWordRd(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list)
	elif(Func == 'DiscWordRd'):
		u16DataWt_list = CopDiscWordRd(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list)
	elif(Func == 'WordWt'):
		u16DataWt_list = CopWordWt(DevID, (FuncCommTable[Func] & 0x7f), DataNum, Addr_list, DataIn_list)
	else:
		pass
		print('ERROR')
		#!!
		return()		
	#透過串列通訊寫入(u16DataWt_list)並回傳回饋資料(u16ReData_list)
	return(SerialWR(DevID, u16DataWt_list, Func, DataNum, RepeatNum))

def SetDate(DevID, Date_y, Date_mth, Date_d, Date_h, Date_min, Date_s):
	#寫入新時間
	Func = 'DiscWordWt'
	DataNum = 6
	ClientOp(DevID, Func, DataNum, [50, 51, 52, 53, 54, 55], [Date_y, Date_mth, Date_d, Date_h, Date_min, Date_s], [], 0)
	#重設新時間
	Func = 'WordWt'
	DataNum = 1
	if (ClientOp(DevID, Func, DataNum, [59], [1], [], 0)):
	#有資料回傳,表示更新成功
		print('SetTiime Work')
	else:
		print('Setting up to fail')
		
	return()	
	
	
def TestPj():
	DevID = 0x01
	Func = 'DiscWordWt'
	DataNum = 2
	#Test Addr Range = 200~1000
	#ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list)
	print(ClientOp(DevID, Func, DataNum, [355, 358], [0xffff,0xeeee],[],0))
	
def TestPj2():
	DevID = 0x01
	Func = 'DiscWordRd'
	DataNum = 2
	#Test Addr Range = 200~1000
	#ClientOp(DevID, Func, DataNum, Addr_list, DataIn_list, Mask_list)
	print(ClientOp(DevID, Func, DataNum, [355, 358],[],[],0))


def TestTimePj():
	DevID = 0x01
	#寫入新時間
	Func = 'DiscWordWt'
	DataNum = 6
	ClientOp(DevID, Func, DataNum, [50, 51, 52, 53, 54, 55], [2015, 6, 1, 6, 15, 0], [], 0)
	#重設新時間
	Func = 'WordWt'
	DataNum = 1
	print(ClientOp(DevID, Func, DataNum, [59], [1], [], 0))
	
def test(DA_list):
	
	return(WordListToAdd3ByteList([1], DA_list))

	
if __name__ == '__main__':

    
	
	#TestPj()
	#TestPj2()
	#TestTimePj()
	print(test([2,3,4]))
