import serial
import time

ser = serial.Serial()

ser.port = "/dev/ttyUSB0"
ser.baudrate = 115200

ser.open()

print ser.isOpen()

if ser.isOpen():

	ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x00\x00\x00\x01\x00\x00\x35\x01\x00')

	time.sleep(3)

	ser.flushInput()
	ser.flushOutput()

	ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x05\x00\x00\x01\x00\x00\x3A\x01\x00')

	time.sleep(1)

	print ser.read(8).encode('hex')
	
	ser.flushInput()
	ser.flushOutput()

	ser.write('\x80\x01\x00\x00\x22\x01\x00\x00\x05\x00\x00\x29\x01\x00')

	time.sleep(1)

	print ser.read(11).encode('hex')
	
	ser.flushInput()
	ser.flushOutput()

	ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x64\x00\x00\x02\x00\x00\x1A\x02\x00')
	time.sleep(.1)
	ser.flushOutput()

	time.sleep(1)

	ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x5A\x00\x00\x08\x27\x00\x3D\x02\x00')
	time.sleep(.1)
	ser.flushOutput()

	time.sleep(1)

	ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x5A\x00\x00\x00\x00\x00\x0E\x02\x00')
	time.sleep(.1)
	ser.flushOutput()
	
	time.sleep(1)

	ser.write('\x80\x01\x00\x00\x32\x01\x00\x00\x5A\x00\x00\x08\x27\x00\x3D\x02\x00')
	time.sleep(.1)
	ser.flushOutput()

	# hme.setDate('2015-10-27 10:33:23')

	ser.close()
