import time
import serial

ser = serial.Serial(
	port = 'dev/ttyAMAO',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

print("khoi dong lai chuong trinh")

try:
	while True
		c = input()
		if c == '1':
			ser.write(b'Raspberry gui xuong')
			ser.flush()
			print ("da gui du lieu")

except KeyboardInterrupt:
    ser.close()
