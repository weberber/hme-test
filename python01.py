import serial
import time

ser = serial.Serial()
ser2 = serial.Serial()

ser.port = "COM16"
ser.baudrate = 115200

ser2.port = "COM17"
ser2.baudrate = 115200

ser.open()
ser2.open()

if ser.isOpen():
        print ("COM16 is OK")
        
if ser2.isOpen():
        print ("COM17 is OK")

#print (ser.isOpen())


x = 0xf0
tstlist=[0x80,0x01,0x02,0x03]


print ( tstlist[0:3] )

if ser.isOpen():

#	ser.write(bytearray('55'))

        ser.write(tstlist[:])



        tStart = time.time()
        while( 50 > tStart - time.time() ):
                print ( ser2.read(2) )

        

ser.close()
ser2.close()

