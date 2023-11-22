import serial
import time
import matplotlib.pyplot as plt
from pylab import *

#ser.write(b'VOLT1 3.141\n')       #ustawienie napięcia SEM1 w [V]
#ser.write(b'VOLT2 6.284\n')       #ustawienie napięcia SEM2 w [V]
#ser.write(b'CURR 2.721\n')        #ustawienie prądu SPM w [mA]
#ser.write(b'MEAS:CURR? (@2)\n')   #pomiar prądu w kan. 2, czyli SEM2
#ser.write(b'MEAS:VOLT? (@3)\n')   #pomiar napięcia w kan. 3, czyli na SPM
#ser.write(b'MEAS:VOLT? (@4)\n')   #pomiar napięcia w kan. 4, czyli wej AUX
#ser.write(b'MEAS:CURR? (@1)\n')   #pomiar prądu w kan. 1, czyli SEM1
#ser.readline()

class Measurement:
    
    def __init__(self, port, bitrate=115200, sleep_time=1, test=False):
        print(f"Trying to open port: {port} at bitrate {bitrate}")
        self.serial = serial.Serial(port, bitrate)
        print(f"Connected to {port}")

        print("Flushing...")
        self.serial.flush()

        self.sleep_time = sleep_time
        self.absSEM1 = False
        self.absSEM2 = False
        self.absSPM = False
        self.absAUX = False

        if test:
            self.testConnection()

        print("Connection is ready.")

    def testConnection(self, values=[0.01, 0.02, 0.03]):
        print("Testing connection with controller...")
        for val in values:
            print(f"[TEST] Value set: {val}")
            self.setSEM1(val)
            self.setSEM2(val)
            self.setSPM(val)
        print("Test ended")

    def sendData(self, msg):
        self.serial.write(bytes(msg,'utf-8')) 
        response = self.serial.readline()
        time.sleep(self.sleep_time)
        return float(response.decode('utf-8'))

    def setSEM1(self, value):
        msg = f'VOLT1 {value}\n'
        self.sendData(msg)

    def setSEM2(self, value):
        msg = f'VOLT2 {value}\n'
        self.sendData(msg)

    def setSPM(self, value):
        msg = f'CURR {value}\n'
        self.sendData(msg)

    def readSEM1(self):
        msg = b'MEAS:CURR? (@1)\n'
        value = self.sendData(msg)
        if self.absSEM1:
            value = abs(value)
        return value
    
    def readSEM2(self):
        msg = b'MEAS:CURR? (@2)\n'
        value = self.sendData(msg)
        if self.absSEM2:
            value = abs(value)
        return value
    
    def readSPM(self):
        msg = b'MEAS:CURR? (@3)\n'
        value = self.sendData(msg)
        if self.absSPM:
            value = abs(value)
        return value
    
    def readAUX(self):
        msg = b'MEAS:CURR? (@4)\n'
        value = self.sendData(msg)
        if self.absAUX:
            value = abs(value)
        return value
    
    def read(self, output_name):
        if output_name=="SEM1":
            return self.readSEM1()
        elif output_name=="SEM2":
            return self.readSEM2()
        elif output_name=="SPM":
            return self.readSPM()
        elif output_name=="AUX":
            return self.readAUX()
        
        return 0
    
    def set(self, input_name, value):
        if input_name=="SEM1":
            self.setSEM1(value)
        elif input_name=="SEM2":
            self.setSEM2(value)
        elif input_name=="SPM":
            self.setSPM(value)

    def measure(self, list_of_values, input_name, output_name):
        output = []
        for val in list_of_values:
            self.set(input_name, val)
            reading = self.read(output_name)
            output.append(reading)
        
        values = ""
        readings = ""
        for val in list_of_values:
            values += f"{val} "
        for read in output:
            readings += f"{read} "
        
        print(f"{input_name}: {values}")
        print(f"{output_name}: {readings}")

        return output
    
    def measureMultiple(self, first_list_of_values, first_input_name, second_list_of_values, second_input_name, output_name):
        output = []
        i=1
        for val in first_list_of_values:
            self.set(first_input_name, val)
            print(f"{i}/{len(first_list_of_values)}   {first_input_name}: {val}")
            i+=1

            subReading = self.measure(second_list_of_values, second_input_name, output_name)
            output.append(subReading)

        return output

    def createGraph(self, x_values, y_values, x_label, y_label, xmin='-', xmax='-', ymin='-', ymax='-'):
        if xmin=='-':
            xmin=x_values[0]
        if xmax=='-':
            xmax=x_values[len(x_values)-1]
        if ymin=='-':
            ymin=y_values[0]
        if ymax=='-':
            ymax=y_values[len(y_values)-1]

        fig, ax = plt.subplots()
        plt.plot( x_values, y_values, label='Tranzystor' )
        ax.grid()
        ax.legend()
        ax.set_xlabel(x_label)                 
        ax.set_ylabel(y_label)                
        ax.axis( [xmin, xmax, ymin, ymax] )      

        plt.show()