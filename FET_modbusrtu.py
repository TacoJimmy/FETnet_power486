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

def read_3p3w_meter(PORT,ID,loop):
    loop = loop - 1
    MainPW_meter = [0,0,0,0,0,0,0,0]
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        pw_va = master.execute(ID, cst.READ_HOLDING_REGISTERS, 4, 1)
        pw_cur = master.execute(ID, cst.READ_HOLDING_REGISTERS, 5+loop*4, 3)
        pw_power = master.execute(ID, cst.READ_HOLDING_REGISTERS, 15+loop*10, 1)
        pw_pf = master.execute(ID, cst.READ_HOLDING_REGISTERS, 24+loop*12, 1)
        pw_consum = master.execute(ID, cst.READ_HOLDING_REGISTERS, 39+loop*4, 2)
        
        MainPW_meter[0] =  round(pw_va[0] * 0.1,1)
        MainPW_meter[1] =  round(pw_cur[0] * 0.01,1)
        MainPW_meter[2] =  round(pw_cur[1] * 0.01,1)
        MainPW_meter[3] =  round(pw_cur[2] * 0.01,1)
        MainPW_meter[4] =  round(pw_power[0] * 0.01,1) 
        MainPW_meter[5] =  round(pw_pf[0]*0.001,1)
        MainPW_meter[6] =  round((pw_consum[1] + pw_consum[0] * 65535)*0.1,1)
        MainPW_meter[7] = 1 
        master.close()
        time.sleep(0.5)
        return (MainPW_meter)
    
    except:
        MainPW_meter[0] = 0
        MainPW_meter[1] = 0
        MainPW_meter[2] = 0
        MainPW_meter[3] = 0
        MainPW_meter[4] = 0
        MainPW_meter[5] = 0
        MainPW_meter[6] = 0
        MainPW_meter[7] = 2
        master.close()
        time.sleep(0.5)
        return (MainPW_meter)

def read_Main_PowerMeter(PORT,ID,loop):
    loop = loop - 1
    MainPW_meter = [0,0,0,0,0,0,0,0]
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        pw_va = master.execute(ID, cst.READ_HOLDING_REGISTERS, 320, 1)
        pw_cur = master.execute(ID, cst.READ_HOLDING_REGISTERS, 321, 6)
        pw_power = master.execute(ID, cst.READ_HOLDING_REGISTERS, 338, 1)
        pw_pf = master.execute(ID, cst.READ_HOLDING_REGISTERS, 358, 1)
        pw_consum = master.execute(ID, cst.READ_HOLDING_REGISTERS, 363, 2)
        
        MainPW_meter[0] = round(pw_va[0] * 0.1,1)
        MainPW_meter[1] = round(pw_cur[1] * 0.01,1)
        MainPW_meter[2] = round(pw_cur[3] * 0.01,1)
        MainPW_meter[3] = round(pw_cur[5] * 0.01,1)
        MainPW_meter[4] = round(pw_power[0] * 0.01,1)
        MainPW_meter[5] = round(pw_pf[0]*0.001,1)
        MainPW_meter[6] = round((pw_consum[0] + pw_consum[1] * 65535)*0.1,1)
        MainPW_meter[7] = 1
        #MainPW_meter[0] =  round(pw_va[0] * 0.1,1)
        #MainPW_meter[1] =  round(pw_cur[0] * 0.01,1)
        #MainPW_meter[2] =  round(pw_cur[1] * 0.01,1)
        #MainPW_meter[3] =  round(pw_cur[2] * 0.01,1)
        #MainPW_meter[4] =  round(pw_power[0] * 0.01,1) 
        #MainPW_meter[5] =  round(pw_pf[0]*0.001,1)
        #MainPW_meter[6] =  round((pw_consum[1] + pw_consum[0] * 65535)*0.1,1)
        #MainPW_meter[7] = 1 
        master.close()
        #time.sleep(0.5)
        return (MainPW_meter)

    except:
        MainPW_meter[0] = 0
        MainPW_meter[1] = 0
        MainPW_meter[2] = 0
        MainPW_meter[3] = 0
        MainPW_meter[4] = 0
        MainPW_meter[5] = 0
        MainPW_meter[6] = 0
        MainPW_meter[7] = 2
        master.close()
        time.sleep(0.5)
        return (MainPW_meter)
 
if __name__ == '__main__':
    #print (getCom1_Power('/dev/ttyS4',9600,3,'INPUT'))
    #air condition 1
    print (read_3p3w_meter('/dev/ttyS1',3,1))
    #air condition 2
    print (read_3p3w_meter('/dev/ttyS1',4,1))
    
    print (read_Main_PowerMeter('/dev/ttyS1',1,1))