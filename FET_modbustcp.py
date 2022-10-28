# coding:utf-8
import codecs
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

def getPowerLoop01(HOST_Addr, HOST_Port, voltage, pf):
    
    clamp32 = {}
    PowerPayload = {}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    try:
        master = modbus_tcp.TcpMaster(host=HOST_Addr,port=HOST_Port)
        master.set_timeout(5.0)
        clamp_data = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 54)
        #print (clamp_data)
        for i in range(27):
            clamp32[i] = ReadFloat((clamp_data[i*2+1], clamp_data[i*2]))
    
        for i in range(3):
            clamp[i]["voltage"]=voltage
            clamp[i]["current_r"]=round(clamp32[i*9])
            clamp[i]["current_s"]=round(clamp32[i*9+3])
            clamp[i]["current_t"]=round(clamp32[i*9+6])
            clamp[i]["temperature_r"]=clamp32[i*9+1]
            clamp[i]["temperature_s"]=clamp32[i*9+4]
            clamp[i]["temperature_t"]=clamp32[i*9+7]
            clamp[i]["battery_r"]=clamp32[i*9+2]
            clamp[i]["battery_s"]=clamp32[i*9+5]
            clamp[i]["battery_t"]=clamp32[i*9+8]
            clamp[i]["power"]= round((380*1.7*(clamp32[i*9]+clamp32[i*9+3]+clamp32[i*9+6]))/1000,1)
            clamp[i]["pf"]= pf
            clamp[i]["alive"]= 1
            payload_data = [{"values":clamp[i]}]
            
    except:
        for i in range(3):
            clamp[i]["voltage"]=i
            clamp[i]["current_r"]=i
            clamp[i]["current_s"]=i
            clamp[i]["current_t"]=i
            clamp[i]["temperature_r"]=i
            clamp[i]["temperature_s"]=i
            clamp[i]["temperature_t"]=i
            clamp[i]["battery_r"]=i
            clamp[i]["battery_s"]=i
            clamp[i]["battery_t"]=i
            clamp[i]["power"]= i
            clamp[i]["pf"]= i
            clamp[i]["alive"]= 2
            payload_data = [{"values":clamp[i]}]
    if clamp[1]["alive"] == 1 :
        clamp[1]["current_r"]=clamp[1]["current_r"]-clamp[0]["current_r"]
        clamp[1]["current_s"]=clamp[1]["current_s"]-clamp[0]["current_s"]
        clamp[1]["current_t"]=clamp[1]["current_t"]-clamp[0]["current_t"]
        clamp[1]["power"]= clamp[1]["power"]-clamp[0]["power"]
    
    with open('static/data/PowerLoop01.json', 'r') as f:
        power_kwh01 = json.load(f)
    f.close
    clamp[0]["power_kwh"] = power_kwh01["power03_kwh"]
    clamp[1]["power_kwh"] = power_kwh01["power04_kwh"]
    clamp[2]["power_kwh"] = power_kwh01["power05_kwh"]
    
    clamp[0]["energy"] = power_kwh01["power03_kwh"]
    clamp[1]["energy"] = power_kwh01["power04_kwh"]
    clamp[2]["energy"] = power_kwh01["power05_kwh"]
    
    clamp[0]["Loop_name"] = "F4NR2_SocketPower"
    clamp[1]["Loop_name"] = "F4NL2_LightPower"
    clamp[2]["Loop_name"] = "F4EL2_BackupPower"
    
    
    
    PowerPayload[0] = [{"access_token": "QIki1lbgrdu9dRcCM4rs",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    PowerPayload[1] = [{"access_token": "khO4exKzLAkZRr9VdrJx",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[1]}]}]
    PowerPayload[2] = [{"access_token": "8G60nMefNfBUeoY7ebm6",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[2]}]}]
    
    with open('static/data/PowerSubLoop03.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    
    with open('static/data/PowerSubLoop04.json', 'w') as f:
        json.dump(PowerPayload[1][0]["data"][0]["values"], f)
    f.close
    
    with open('static/data/PowerSubLoop05.json', 'w') as f:
        json.dump(PowerPayload[2][0]["data"][0]["values"], f)
    f.close
    
    return PowerPayload

def getPowerLoop02(HOST_Addr, HOST_Port, voltage, pf):
    
    clamp32 = {}
    PowerPayload = {}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    try:
        master = modbus_tcp.TcpMaster(host=HOST_Addr,port=HOST_Port)
        master.set_timeout(5.0)
        clamp_data = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 54)
        #print (clamp_data)
        for i in range(27):
            clamp32[i] = ReadFloat((clamp_data[i*2+1], clamp_data[i*2]))
    
        for i in range(3):
            clamp[i]["voltage"]=voltage
            clamp[i]["current_r"]=clamp32[i*9]
            clamp[i]["current_s"]=clamp32[i*9+3]
            clamp[i]["current_t"]=clamp32[i*9+6]
            clamp[i]["temperature_r"]=clamp32[i*9+1]
            clamp[i]["temperature_s"]=clamp32[i*9+4]
            clamp[i]["temperature_t"]=clamp32[i*9+7]
            clamp[i]["battery_r"]=clamp32[i*9+2]
            clamp[i]["battery_s"]=clamp32[i*9+5]
            clamp[i]["battery_t"]=clamp32[i*9+8]
            clamp[i]["power"]= round((380*1.7*(clamp32[i*9]+clamp32[i*9+3]+clamp32[i*9+6]))/1000,1)
            clamp[i]["pf"]= pf
            clamp[i]["alive"]= 1
            payload_data = [{"values":clamp[i]}]
            
    except:
        for i in range(3):
            clamp[i]["voltage"]=i
            clamp[i]["current_r"]=i
            clamp[i]["current_s"]=i
            clamp[i]["current_t"]=i
            clamp[i]["temperature_r"]=i
            clamp[i]["temperature_s"]=i
            clamp[i]["temperature_t"]=i
            clamp[i]["battery_r"]=i
            clamp[i]["battery_s"]=i
            clamp[i]["battery_t"]=i
            clamp[i]["power"]= i
            clamp[i]["pf"]= i
            clamp[i]["alive"]= 2
            payload_data = [{"values":clamp[i]}]
    
    if clamp[1]["alive"] == 1 :
        clamp[1]["current_r"]=clamp[1]["current_r"]-clamp[2]["current_r"]
        clamp[1]["current_s"]=clamp[1]["current_s"]-clamp[2]["current_s"]
        clamp[1]["current_t"]=clamp[1]["current_t"]-clamp[2]["current_t"]
        clamp[1]["power"]= clamp[1]["power"]-clamp[2]["power"]
    
    with open('static/data/PowerLoop02.json', 'r') as f:
        power_kwh02 = json.load(f)
    f.close
    clamp[0]["power_kwh"] = power_kwh02["power06_kwh"]
    clamp[1]["power_kwh"] = power_kwh02["power07_kwh"]
    clamp[2]["power_kwh"] = power_kwh02["power08_kwh"]
    clamp[0]["energy"] = power_kwh02["power06_kwh"]
    clamp[1]["energy"] = power_kwh02["power07_kwh"]
    clamp[2]["energy"] = power_kwh02["power08_kwh"]
    
    
    clamp[0]["Loop_name"] = "F4EL1_BackupPower"
    clamp[1]["Loop_name"] = "F4NL1_LightPower"
    clamp[2]["Loop_name"] = "F4NR1_SocketPower"
    
    PowerPayload[0] = [{"access_token": "W8tpPG6jB0Ju3ogOxQoQ",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    PowerPayload[1] = [{"access_token": "Zl0fvlfa7ZJAo8cX7RvO",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[1]}]}]
    PowerPayload[2] = [{"access_token": "T6bEocUJOy7xaCyR0z62",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[2]}]}]

    
    with open('static/data/PowerSubLoop08.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    
    with open('static/data/PowerSubLoop07.json', 'w') as f:
        json.dump(PowerPayload[1][0]["data"][0]["values"], f)
    f.close
    
    with open('static/data/PowerSubLoop06.json', 'w') as f:
        json.dump(PowerPayload[2][0]["data"][0]["values"], f)
    f.close


    return PowerPayload
    
def CleanPowerFlag():
    with open('static/data/PowerLoop01.json', 'r') as f:
        Power_data = json.load(f)
    Power_data["Power_Flag"] = 0
    with open('static/data/PowerLoop01.json', 'w') as g:
        json.dump(Power_data, g)
    f.close
    
    
def power_count():
    power_kwh01 = {}
    power_kwh02 = {}
    powermeter01 = (getPowerLoop01('192.168.1.10',502,380,0.9))
    
    
    with open('static/data/PowerLoop01.json', 'r') as f:
        power_kwh01 = json.load(f)
    f.close
    power_kwh01["power03_kwh"]=power_kwh01["power03_kwh"] + (powermeter01[0][0]["data"][0]["values"]["power"]/240)
    power_kwh01["power04_kwh"]=power_kwh01["power04_kwh"] + (powermeter01[1][0]["data"][0]["values"]["power"]/240)
    power_kwh01["power05_kwh"]=power_kwh01["power05_kwh"] + (powermeter01[2][0]["data"][0]["values"]["power"]/240)
    
    with open('static/data/PowerLoop01.json', 'w') as g:
        json.dump(power_kwh01, g)
    g.close
    
    
    powermeter02 = (getPowerLoop02('192.168.1.11',502,380,0.9))
    
    with open('static/data/PowerLoop02.json', 'r') as f:
        power_kwh02 = json.load(f)
    f.close
    power_kwh02["power06_kwh"]=power_kwh02["power06_kwh"] + (powermeter02[0][0]["data"][0]["values"]["power"]/240)
    power_kwh02["power07_kwh"]=power_kwh02["power07_kwh"] + (powermeter02[1][0]["data"][0]["values"]["power"]/240)
    power_kwh02["power08_kwh"]=power_kwh02["power08_kwh"] + (powermeter02[2][0]["data"][0]["values"]["power"]/240)
    with open('static/data/PowerLoop02.json', 'w') as g:
        json.dump(power_kwh02, g)
    g.close
    
    
if __name__ == '__main__':
    
    power_kwh01 = {}
    power_kwh02 = {}
    powermeter01 = (getPowerLoop01('192.168.1.10',502,380,0.9))
    print (powermeter01[0][0]["data"][0]["values"]["power"])
    print (powermeter01[1][0]["data"][0]["values"]["power"])
    print (powermeter01[2][0]["data"][0]["values"]["power"])
    
    with open('static/data/PowerLoop01.json', 'r') as f:
        power_kwh01 = json.load(f)
    f.close
    power_kwh01["power03_kwh"]=power_kwh01["power03_kwh"] + (powermeter01[0][0]["data"][0]["values"]["power"]/60)
    power_kwh01["power04_kwh"]=power_kwh01["power04_kwh"] + (powermeter01[1][0]["data"][0]["values"]["power"]/60)
    power_kwh01["power05_kwh"]=power_kwh01["power05_kwh"] + (powermeter01[2][0]["data"][0]["values"]["power"]/60)
    with open('static/data/PowerLoop01.json', 'w') as g:
        json.dump(power_kwh01, g)
    g.close
    print (power_kwh01["power03_kwh"])
    print (power_kwh01["power04_kwh"])
    print (power_kwh01["power05_kwh"])
    
    time.sleep(2)
    powermeter02 = (getPowerLoop02('192.168.1.11',502,380,0.9))
    print (powermeter02[0][0]["data"][0]["values"]["power"])
    print (powermeter02[1][0]["data"][0]["values"]["power"])
    print (powermeter02[2][0]["data"][0]["values"]["power"])
    with open('static/data/PowerLoop02.json', 'r') as f:
        power_kwh02 = json.load(f)
    f.close
    power_kwh02["power06_kwh"]=power_kwh02["power06_kwh"] + (powermeter02[0][0]["data"][0]["values"]["power"]/60)
    power_kwh02["power07_kwh"]=power_kwh02["power07_kwh"] + (powermeter02[1][0]["data"][0]["values"]["power"]/60)
    power_kwh02["power08_kwh"]=power_kwh02["power08_kwh"] + (powermeter02[2][0]["data"][0]["values"]["power"]/60)
    with open('static/data/PowerLoop02.json', 'w') as g:
        json.dump(power_kwh02, g)
    g.close
    print (power_kwh02["power06_kwh"])
    print (power_kwh02["power07_kwh"])
    print (power_kwh02["power08_kwh"])