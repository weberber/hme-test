import serial
import time

ser = serial.Serial()
ser2 = serial.Serial()

ser.port = "/dev/ttyUSB2"
ser.baudrate = 115200

ser2.port = "/dev/ttyUSB3"
ser2.baudrate = 115200
ser2.timeout = None

ser.open()
ser2.open()

if ser.isOpen():
        print ("USB1 is OK")
        
if ser2.isOpen():
        print ("USB2 is OK")

#print (ser.isOpen())


x = 0xf0
tstlist=[0x80,0x01,0x02,0x03,0x01,0x02,0x03,0x01,0x02,0x03,0x01,0x02,0x03]


print ( tstlist[0:3] )

if ser.isOpen():

#	ser.write(bytearray('55'))

        ser.write(tstlist[:])

        i = 0

        
        print ("Test is Start")  
        tStart = time.time()
        while( (1 > ( time.time() - tStart )) ):
                if ser2.inWaiting():
                        print ( ser2.read(ser2.inWaiting()) )
                i = i + 1
                print (   time.time() - tStart )
                print ( i )

print ("Test is Over")     

ser.close()
ser2.close()
