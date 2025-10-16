import serial

try:
    ser = serial.Serial("/dev/ttyUSB0", 1000000, timeout=1)
    print("Port opened successfully!")
    ser.close()
except Exception as e:
    print("Error:", e)

