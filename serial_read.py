import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
def openport():
    portlist = []

    for OnePort in ports:
        portlist.append(str(OnePort))
        print(str(OnePort))
    val = input("select port COM:")

    serialInst.baudrate = 57600
    serialInst.port = ("Com" + str(val))
    serialInst.open()
def read():
    while True:
        if serialInst.inWaiting():
            packet = serialInst.readline()
            return float(packet.decode("utf").rstrip("\n"))

