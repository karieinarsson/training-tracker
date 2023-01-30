import serial
import glob
import sys

def get_speed(bluetooth):
    while True:
        data = get_data(bluetooth)
        if data is None:
            return
        aX, aY, aZ, time, samples, sample_rate = data
        vZ = derivate(aZ, sample_rate)
        print(f"Top Speed: {round(max(vZ), 3)}")
        return round(max(vZ), 3)

def connect_bt(port):
    bluetooth=serial.Serial(port, 9600)
    bluetooth.flushInput()
    return bluetooth

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def get_data(bluetooth):
    data = bluetooth.readline()
    data = data.decode()
    if data == "":
        return
    data = data.split(";")
    for i in range(len(data)):
        data[i] = data[i].split(",")
    samples = int(data[4][0])
    time = int(data[3][0])
    
    sample_rate = time/(samples*1000)
    
    aX = [eval(i) for i in data[0][:-1]]
    aY = [eval(i) for i in data[1][:-1]]
    aZ = [eval(i) for i in data[2][:-1]]

    assert len(aX) == samples, "Did not recieve all samples"
    
    return aX, aY, aZ, time, samples, sample_rate


def derivate(list, sample_rate):
    current_value = 0
    return_list = []
    for val in list:
        current_value += val*sample_rate*9.82
        return_list.append(current_value)
    return return_list


if __name__ == "__main__":
    print(serial_ports())