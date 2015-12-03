import serial
import time

ser = serial.Serial()

ser.port = "COM16"
ser.baudrate = 115200

ser.open()

print (ser.isOpen())

x = 0xf0
tstlist=[0x80,0x01,0x00,0x00,0x32,0x01,
         0x00,0x00,0x05,0x00,0x00,0x01,0x00,0x00,0x3A,0x01,0x00]


print ( tstlist[3:8] )

if ser.isOpen():

#	ser.write(bytearray('55'))

        ser.write(tstlist[:])



        tStart = time.time()
        while( 50 > tStart - time.time() ):
                print ( ser.read(1) )

        

ser.close()
