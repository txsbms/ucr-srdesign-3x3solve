import serial
import time

serialPayloadB = ["L1,LP,L2,U1,UP,U2,R1,RP,R2,F1,FP,F2,B1,BP,B2"]

if __name__ == '__main__':
    print("Opening Serial Port...")
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    time.sleep(2)
    
    for i in range(len(serialPayloadB)):
        ser.write(serialPayloadB[i].encode('ASCII'))
        time.sleep(0.05)
    line = ser.readline().decode('ASCII').rstrip()
    print(line)
