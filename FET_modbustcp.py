import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import struct
import paho.mqtt.client as mqtt
import random
import json  
import datetime 
import time

def conver32(LSB,MSB):
    conv32value = LSB + ( MSB << 16 )
    return (conv32value)

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

def PowerLoop():
    with open('static/data/PowerMeter.json', 'r') as f:
        data = json.load(f)
    f.close
    return data

def getPowerLoop01(HOST_Addr, HOST_Port):
    
    clamp32 = {}
    PowerPayload = {}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    try:
        master = modbus_tcp.TcpMaster(host=HOST_Addr,port=HOST_Port)
        master.set_timeout(5.0)
        clamp_data = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 54)
        print (clamp_data)
        for i in range(27):
            clamp32[i] = ReadFloat((clamp_data[i*2+1], clamp_data[i*2]))
    
        for i in range(3):
            clamp[i]["voltage"]="380"
            clamp[i]["current_r"]=str(clamp32[i*9])
            clamp[i]["current_s"]=str(clamp32[i*9+3])
            clamp[i]["current_t"]=str(clamp32[i*9+6])
            clamp[i]["temperature_r"]=str(clamp32[i*9+1])
            clamp[i]["temperature_s"]=str(clamp32[i*9+4])
            clamp[i]["temperature_t"]=str(clamp32[i*9+7])
            clamp[i]["battery_r"]=str(clamp32[i*9+2])
            clamp[i]["battery_s"]=str(clamp32[i*9+5])
            clamp[i]["battery_t"]=str(clamp32[i*9+8])
            clamp[i]["power"]= str(round((380*1.7*(clamp32[i*9]+clamp32[i*9+3]+clamp32[i*9+6]))/1000,1))
            clamp[i]["pf"]= str(0.9)
            clamp[i]["alive"]= str(1)
            payload_data = [{"values":clamp[i]}]
            
    except:
        for i in range(3):
            clamp[i]["voltage"]=str(i)
            clamp[i]["current_r"]=str(i)
            clamp[i]["current_s"]=str(i)
            clamp[i]["current_t"]=str(i)
            clamp[i]["temperature_r"]=str(i)
            clamp[i]["temperature_s"]=str(i)
            clamp[i]["temperature_t"]=str(i)
            clamp[i]["battery_r"]=str(i)
            clamp[i]["battery_s"]=str(i)
            clamp[i]["battery_t"]=str(i)
            clamp[i]["power"]= str(i)
            clamp[i]["pf"]= str(i)
            clamp[i]["alive"]= 2
            payload_data = [{"values":clamp[i]}]
            
    
    
    PowerPayload[0] = [{"access_token": "RtKzCEgphGCq53CrCvq3",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    PowerPayload[1] = [{"access_token": "eEUb9N4SbTHpblayLA5Q",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[1]}]}]
    PowerPayload[2] = [{"access_token": "QIki1lbgrdu9dRcCM4rs",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[2]}]}]

    
    return PowerPayload

def getPowerLoop02(HOST_Addr, HOST_Port):
    
    clamp32 = {}
    PowerPayload = {}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    try:
        master = modbus_tcp.TcpMaster(host=HOST_Addr,port=HOST_Port)
        master.set_timeout(5.0)
        clamp_data = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 54)
        print (clamp_data)
        for i in range(27):
            clamp32[i] = ReadFloat((clamp_data[i*2+1], clamp_data[i*2]))
    
        for i in range(3):
            clamp[i]["voltage"]="380"
            clamp[i]["current_r"]=str(clamp32[i*9])
            clamp[i]["current_s"]=str(clamp32[i*9+3])
            clamp[i]["current_t"]=str(clamp32[i*9+6])
            clamp[i]["temperature_r"]=str(clamp32[i*9+1])
            clamp[i]["temperature_s"]=str(clamp32[i*9+4])
            clamp[i]["temperature_t"]=str(clamp32[i*9+7])
            clamp[i]["battery_r"]=str(clamp32[i*9+2])
            clamp[i]["battery_s"]=str(clamp32[i*9+5])
            clamp[i]["battery_t"]=str(clamp32[i*9+8])
            clamp[i]["power"]= str(round((380*1.7*(clamp32[i*9]+clamp32[i*9+3]+clamp32[i*9+6]))/1000,1))
            clamp[i]["pf"]= str(0.9)
            clamp[i]["alive"]= str(1)
            payload_data = [{"values":clamp[i]}]
            
    except:
        for i in range(3):
            clamp[i]["voltage"]=str(i)
            clamp[i]["current_r"]=str(i)
            clamp[i]["current_s"]=str(i)
            clamp[i]["current_t"]=str(i)
            clamp[i]["temperature_r"]=str(i)
            clamp[i]["temperature_s"]=str(i)
            clamp[i]["temperature_t"]=str(i)
            clamp[i]["battery_r"]=str(i)
            clamp[i]["battery_s"]=str(i)
            clamp[i]["battery_t"]=str(i)
            clamp[i]["power"]= str(i)
            clamp[i]["pf"]= str(i)
            clamp[i]["alive"]= 2
            payload_data = [{"values":clamp[i]}]
            
    
    
    PowerPayload[0] = [{"access_token": "khO4exKzLAkZRr9VdrJx",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    PowerPayload[1] = [{"access_token": "8G60nMefNfBUeoY7ebm6",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[1]}]}]
    PowerPayload[2] = [{"access_token": "T6bEocUJOy7xaCyR0z62",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[2]}]}]

    
    return PowerPayload

def SavePowerLoop():
    PowerLoop01 = getPowerLoop01('HOST_Addr', 'HOST_Port')
    with open('static/data/PowerLoop01.json', 'w') as f:
        json.dump(PowerLoop01, f)
    f.close
    
    PowerLoop02 = getPowerLoop01('HOST_Addr', 'HOST_Port')
    with open('static/data/PowerLoop02.json', 'w') as f:
        json.dump(PowerLoop02, f)
    f.close
    
def CleanPowerFlag():
    with open('static/data/PowerLoop01.json', 'r') as f:
        Power_data = json.load(f)
    Power_data["Power_Flag"] = 0
    with open('static/data/PowerLoop01.json', 'w') as g:
        json.dump(Power_data, g)
    f.close
    
if __name__ == '__main__':
    print(getPowerLoop01('192.168.1.10',502))
    time.sleep(2)
    print(getPowerLoop02('192.168.1.11',502))
    #SavePowerLoop()
    
    #CleanPowerFlag()