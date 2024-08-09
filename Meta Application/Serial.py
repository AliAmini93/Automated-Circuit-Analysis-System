import serial.tools.list_ports
import serial

def check_com_port():
    # Find the COM port connected
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "COM" in port:
            try:
                ser = serial.Serial(port, 115200)
                ser.close()
                print(f"COM port found: {port}")
                return True
            except serial.SerialException as e:
                print(f"Error opening port {port}: {e}")
                continue
    else:
        print("No COM port detected")
        return False
def calibrate():
    # Find the COM port connected
    ports = serial.tools.list_ports.comports()
    ser = None  # Initialize ser variable before the loop
    for port, desc, hwid in sorted(ports):
        if "COM" in port:
            try:
                ser = serial.Serial(port, 115200)
                print(f"Connected to {port}")
                break
            except serial.SerialException as e:
                print(f"Error opening port {port}: {e}")
                continue
    else:
        print("No COM port detected")
        return False  # Return False if no COM port is detected
        
    # Send the commands
    commands = ["010D0000000000000E", "010D00020000000010", "010D00040000000012"]
    for command in commands:
        ser.write(bytes.fromhex(command))
        #response = ser.readline()
        #print(response)
    
    # Close the serial port
    ser.close()
    print("Serial port closed")
    return True # Return True if the calibration process is successful
'''
# Example usage in your PyQt5 application
calibration_status = calibrate()
if calibration_status:
    print("Calibration successful")
else:
    print("Calibration failed")
'''
