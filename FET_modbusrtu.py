import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

def getCom1_Power(ComPort,BbaudRate,ID,Func):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=ComPort, baudrate=BbaudRate, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        if Func == "INPUT":
            AC_status = master.execute(ID, cst.READ_INPUT_REGISTERS, 3, 1)
        if Func == "HOLDING":
            AC_status = master.execute(ID, cst.READ_HOLDING_REGISTERS, 3, 1)
        time.sleep(0.5)
        return (AC_status[0])
        
    except:
        master.close()
        return ('loss_connect')
    
if __name__ == '__main__':
    print (getCom1_Power('COM3',9600,104,'INPUT'))