# coding:utf-8
import codecs
import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import json  
import struct

def ReadFloat(*args,reverse=False):
    for n,m in args:
        n,m = '%04x'%n,'%04x'%m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f',y_bytes)[0]
    y = round(y,6)
    return y

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
        pw_consum = master.execute(ID, cst.READ_HOLDING_REGISTERS, 385, 2)
        
        MainPW_meter[0] = round(pw_va[0] * 0.1,1)
        MainPW_meter[1] = round(pw_cur[1] * 0.001,1)
        MainPW_meter[2] = round(pw_cur[3] * 0.001,1)
        MainPW_meter[3] = round(pw_cur[5] * 0.001,1)
        MainPW_meter[4] = round(pw_power[0] * 0.01,1)
        MainPW_meter[5] = pw_pf[0]
        MainPW_meter[5] = ReadFloat((pw_consum[0],pw_consum[1]))
        #MainPW_meter[6] = round((pw_consum[1] + pw_consum[0] * 65535)*0.1,1)
        #MainPW_meter[6] = round(pw_consum[0],1)
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
'''
def get_subloop01():
    
    PowerPayload = {}
    powerloop01 = read_Main_PowerMeter('/dev/ttyS1',1,1)
    powerloop02 = read_Main_PowerMeter('/dev/ttyS1',2,1)
    
    PowerPayload[0] = [{"access_token": "WImETF1BotX8l1xIkZ3K",
             "app": "ems_demo_fet",
             "type": "3P4WMETER",
             "data": [{"values":powerloop01[0]}]}]
    PowerPayload[1] = [{"access_token": "wFeXyzMjZvTB4hhZ6a1c",
             "app": "ems_demo_fet",
             "type": "3P4WMETER",
             "data": [{"values":powerloop02[1]}]}]
    
    with open('static/data/PowerSubLoop01.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    
    with open('static/data/PowerSubLoop02.json', 'w') as f:
        json.dump(PowerPayload[1][0]["data"][0]["values"], f)
    f.close
    
    return PowerPayload
'''
   
def get_MainPayLoad(payload1,payload2):
    PowerPayload = {}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    
    try:
        clamp[0]["voltage"]=round(payload1[0])
        clamp[0]["current_r"]=round(payload1[1],1)
        clamp[0]["current_s"]=round(payload1[2],1)
        clamp[0]["current_t"]=round(payload1[3],1)
        clamp[0]["temperature_r"]=0
        clamp[0]["temperature_s"]=0
        clamp[0]["temperature_t"]=0
        clamp[0]["power"]= round(payload1[4],1)
        clamp[0]["pf"]= round(payload1[5]*100)
        clamp[0]["energy"] = round(payload1[6],1)
        clamp[0]["alive"]= 1
        payload_data = [{"values":clamp}]

        clamp[1]["voltage"]=round(payload2[0])
        clamp[1]["current_r"]=round(payload2[1],1)
        clamp[1]["current_s"]=round(payload2[2],1)
        clamp[1]["current_t"]=round(payload2[3],1)
        clamp[1]["temperature_r"]=0
        clamp[1]["temperature_s"]=0
        clamp[1]["temperature_t"]=0
        clamp[1]["power"]= round(payload2[4],1)
        clamp[1]["pf"]= round(payload2[5]*100)
        clamp[1]["energy"] = round(payload2[6],1)
        clamp[1]["alive"]= 1
        payload_data = [{"values":clamp}]
    except:
        for i in range(2):
            clamp[i]["voltage"]=0
            clamp[i]["current_r"]=0
            clamp[i]["current_s"]=0
            clamp[i]["current_t"]=0
            clamp[i]["temperature_r"]=0
            clamp[i]["temperature_s"]=0
            clamp[i]["temperature_t"]=0
            clamp[i]["battery_r"]=0
            clamp[i]["battery_s"]=0
            clamp[i]["battery_t"]=0
            clamp[i]["power"]= 0
            clamp[i]["pf"]= 0
            clamp[i]["alive"]= 2
        payload_data = [{"values":clamp}]
            
    clamp[0]["Loop_name"] = "F4NP1_normalpower"
    clamp[1]["Loop_name"] = "F4EP1_backuppower"
    
    PowerPayload[0] = [{"access_token": "WImETF1BotX8l1xIkZ3K",
             "app": "ems_demo_fet",
             "type": "3P4WMETER",
             "data": [{"values":clamp[0]}]}]
    PowerPayload[1] = [{"access_token": "wFeXyzMjZvTB4hhZ6a1c",
             "app": "ems_demo_fet",
             "type": "3P4WMETER",
             "data": [{"values":clamp[1]}]}]
    
    with open('static/data/PowerMainLoop01.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    with open('static/data/PowerMainLoop02.json', 'w') as f:
        json.dump(PowerPayload[1][0]["data"][0]["values"], f)
    f.close
    
    return PowerPayload

def get_ACPayLoad(payload1,payload2):
    PowerPayload = {}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    
    try:
        clamp[0]["voltage"]=payload1[0]
        clamp[0]["current_r"]=payload1[1]
        clamp[0]["current_s"]=payload1[2]
        clamp[0]["current_t"]=payload1[3]
        clamp[0]["temperature_r"]=0
        clamp[0]["temperature_s"]=0
        clamp[0]["temperature_t"]=0
        clamp[0]["power"]= payload1[4]
        clamp[0]["pf"]= payload1[5]
        clamp[0]["energy"] = payload1[6]
        clamp[0]["alive"]= 1
        payload_data = [{"values":clamp}]

        clamp[1]["voltage"]=payload2[0]
        clamp[1]["current_r"]=payload2[1]
        clamp[1]["current_s"]=payload2[2]
        clamp[1]["current_t"]=payload2[3]
        clamp[1]["temperature_r"]=0
        clamp[1]["temperature_s"]=0
        clamp[1]["temperature_t"]=0
        clamp[1]["power"]= payload2[4]
        clamp[1]["pf"]= payload2[5]
        clamp[1]["energy"] = payload2[6]
        clamp[1]["alive"]= 1
        payload_data = [{"values":clamp}]
    except:
        for i in range(2):
            clamp[i]["voltage"]=0
            clamp[i]["current_r"]=0
            clamp[i]["current_s"]=0
            clamp[i]["current_t"]=0
            clamp[i]["temperature_r"]=0
            clamp[i]["temperature_s"]=0
            clamp[i]["temperature_t"]=0
            clamp[i]["battery_r"]=0
            clamp[i]["battery_s"]=0
            clamp[i]["battery_t"]=0
            clamp[i]["power"]= 0
            clamp[i]["pf"]= 0
            clamp[i]["alive"]= 2
        payload_data = [{"values":clamp}]
            
    clamp[0]["Loop_name"] = "F4NP2_nomal_ACPower"
    clamp[1]["Loop_name"] = "F4EP2_backup_ACPower"    
    
    PowerPayload[0] = [{"access_token": "RtKzCEgphGCq53CrCvq3",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    PowerPayload[1] = [{"access_token": "eEUb9N4SbTHpblayLA5Q",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[1]}]}]
    
    with open('static/data/PowerSubLoop01.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    
    with open('static/data/PowerSubLoop02.json', 'w') as f:
        json.dump(PowerPayload[1][0]["data"][0]["values"], f)
    f.close
    
    return PowerPayload

if __name__ == '__main__':
    
    print(read_Main_PowerMeter('/dev/ttyS1',1,1))
    print(read_Main_PowerMeter('/dev/ttyS1',2,1))
    '''
    #print (getCom1_Power('/dev/ttyS1',1,1))
    #air condition 1
    #print (read_3p3w_meter('/dev/ttyS1',3,1))
    #air condition 2
    #print (read_3p3w_meter('/dev/ttyS1',4,1))
    
    SubACLoop01 = read_3p3w_meter('/dev/ttyS1',3,1)
    print(SubACLoop01)
    SubACLoop02 = read_3p3w_meter('/dev/ttyS1',4,1)
    print(SubACLoop02)
    
    print (get_ACPayLoad(SubACLoop01,SubACLoop02))
    
    #print (read_Main_PowerMeter('/dev/ttyS1',1,1))
    #print (read_Main_PowerMeter('/dev/ttyS1',2,1))
    '''