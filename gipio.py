#!/usr/bin/python3
import time
import serial

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=9600,
    timeout=0.5,

)

# Wait a second to let the port initialize
time.sleep(1)

arduino_message = ""
wait = True


try:
    ##while True:
    text = "Mensaje\r\n"
    for i in text:
        serial_port.write(i.encode('utf-8'))
        time.sleep(0.1)   
    wait = True         
    while wait:
        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            arduino_message = arduino_message + data.decode('utf-8')
            if data == "\n".encode():
                wait = False
                print(arduino_message)
                arduino_message = ""

    #serial_port.write("NVIDIA Jetson Nano Developer Kit\r\n".encode())
    """ while True:
        text = input("Input message: ")
        print("Sending:", text)
        text = text + "\n"
        print(text.encode())
        for i in text:
            serial_port.write(i.encode('utf-8'))
            time.sleep(0.1)
        wait = True
        #while wait:
        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            print(data)
            arduino_message = arduino_message + data.decode('utf-8')
            if data == "\n".encode():
                wait = False
                print(arduino_message)
                arduino_message = "" """

except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass