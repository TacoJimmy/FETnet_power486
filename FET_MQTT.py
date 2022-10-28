# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time
import FET_modbustcp
import FET_modbusrtu

def PowerLoop():
    with open('static/data/PowerMeter.json', 'r') as f:
        data = json.load(f)
    f.close
    return data

def ReadMqttInfor():
    with open('static/data/mqttinfor.json', 'r') as f:
        data = json.load(f)
    f.close
    return data

def MqttSend(mod_payload):
    Mqttinfor = ReadMqttInfor()
    try:
        client = mqtt.Client('', True, None, mqtt.MQTTv31)
        client.username_pw_set(Mqttinfor['appInfo']['MQTT_UserName'], Mqttinfor['appInfo']['MQTT_Password'])
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client.tls_set_context(context)
        client.connect(Mqttinfor['appInfo']['MQTT_url'], Mqttinfor['appInfo']['MQTT_Port'], 60)
        client.loop_start()
        time.sleep(1)
        data02 = client.on_connect
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[0]))
        time.sleep(1)
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[1]))
        time.sleep(1)
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[2]))
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
        time.sleep(1)
    except:
        print ('error')
        return ('error')

def MqttMainSend(mod_payload):
    Mqttinfor = ReadMqttInfor()
    try:
        client = mqtt.Client('', True, None, mqtt.MQTTv31)
        client.username_pw_set(Mqttinfor['appInfo']['MQTT_UserName'], Mqttinfor['appInfo']['MQTT_Password'])
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client.tls_set_context(context)
        client.connect(Mqttinfor['appInfo']['MQTT_url'], Mqttinfor['appInfo']['MQTT_Port'], 60)
        client.loop_start()
        time.sleep(1)
        data02 = client.on_connect
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[0]))
        time.sleep(2)
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[1]))
        time.sleep(2)
        client.loop_stop()
        client.disconnect()
        time.sleep(1)
    except:
        print ('error')
        return ('error')

def MqttACSend(mod_payload):
    Mqttinfor = ReadMqttInfor()
    try:
        client = mqtt.Client('', True, None, mqtt.MQTTv31)
        client.username_pw_set(Mqttinfor['appInfo']['MQTT_UserName'], Mqttinfor['appInfo']['MQTT_Password'])
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client.tls_set_context(context)
        client.connect(Mqttinfor['appInfo']['MQTT_url'], Mqttinfor['appInfo']['MQTT_Port'], 60)
        client.loop_start()
        time.sleep(1)
        data02 = client.on_connect
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[0]))
        time.sleep(2)
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(mod_payload[1]))
        time.sleep(2)
        client.loop_stop()
        client.disconnect()
        time.sleep(1)
    except:
        print ('error')
        return ('error')

def Mainloop01Cal():
    try:
        clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
        PowerPayload = {}
        with open('static/data/PowerSubLoop03.json', 'r') as f:
            F4NR2_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop04.json', 'r') as f:
            F4NL2_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop05.json', 'r') as f:
            F4EL2_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop06.json', 'r') as f:
            F4EL1_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop07.json', 'r') as f:
            F4NL1_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop08.json', 'r') as f:
            F4NR1_data = json.load(f)
        f.close
        clamp[0]["voltage"] = F4NR2_data["voltage"]
        clamp[0]["current_r"]= F4NR2_data["current_r"] + F4NL2_data["current_r"] + F4NL1_data["current_r"]
        clamp[0]["current_s"]= F4NR2_data["current_s"] + F4NL2_data["current_s"] + F4NL1_data["current_s"]
        clamp[0]["current_t"]= F4NR2_data["current_t"] + F4NL2_data["current_t"] + F4NL1_data["current_t"]
        clamp[0]["temperature_r"]= 30
        clamp[0]["temperature_s"]= 30
        clamp[0]["temperature_t"]= 30
        clamp[0]["battery_r"]= 2
        clamp[0]["battery_s"]= 2
        clamp[0]["battery_t"]= 2
        clamp[0]["power"]= F4NR2_data["power"] + F4NL2_data["power"] + F4NL1_data["power"]
        clamp[0]["pf"]= F4NR2_data["pf"]
        clamp[0]["alive"]= 1   
        
        
    except:
        clamp[0]["alive"]= 0
        
    clamp[0]["Loop_name"]= "F4NP1_常用總電源"
    
    PowerPayload[0] = [{"access_token": "WImETF1BotX8l1xIkZ3K",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    
    with open('static/data/PowerMainLoop01.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    
    return PowerPayload
    
def Mainloop02Cal():
    try:
        clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
        PowerPayload = {}
        with open('static/data/PowerSubLoop03.json', 'r') as f:
            F4NR2_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop04.json', 'r') as f:
            F4NL2_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop05.json', 'r') as f:
            F4EL2_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop06.json', 'r') as f:
            F4EL1_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop07.json', 'r') as f:
            F4NL1_data = json.load(f)
        f.close
        with open('static/data/PowerSubLoop08.json', 'r') as f:
            F4NR1_data = json.load(f)
        f.close
        clamp[0]["voltage"] = F4EL1_data["voltage"]
        clamp[0]["current_r"]= F4EL1_data["current_r"] + F4EL2_data["current_r"]
        clamp[0]["current_s"]= F4EL1_data["current_s"] + F4EL2_data["current_s"]
        clamp[0]["current_t"]= F4EL1_data["current_t"] + F4EL2_data["current_t"]
        clamp[0]["temperature_r"]= 30
        clamp[0]["temperature_s"]= 30
        clamp[0]["temperature_t"]= 30
        clamp[0]["battery_r"]= 2
        clamp[0]["battery_s"]= 2
        clamp[0]["battery_t"]= 2
        clamp[0]["power"]= F4EL1_data["power"] + F4EL2_data["power"] 
        clamp[0]["pf"]= F4EL1_data["pf"]
        clamp[0]["alive"]= 1   
        
        
    except:
        clamp[0]["alive"]= 0
        
    clamp[0]["Loop_name"]= "F4NE1_備用總電源"
    
    PowerPayload[0] = [{"access_token": "wFeXyzMjZvTB4hhZ6a1c",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    
    with open('static/data/PowerMainLoop02.json', 'w') as f:
        json.dump(PowerPayload[0][0]["data"][0]["values"], f)
    f.close
    
    return PowerPayload
    
def MqttPublish():
    try:
        #PowerInfor = PowerLoop()
        
        MainLoop01 = FET_modbusrtu.read_Main_PowerMeter('/dev/ttyS1',1,1)
        MainLoop02 = FET_modbusrtu.read_Main_PowerMeter('/dev/ttyS1',2,1)
        MainPayload = FET_modbusrtu.get_MainPayLoad(MainLoop01,MainLoop02)
        #print(MainPayload)
        MqttMainSend(MainPayload)
        
        SubACLoop01 = FET_modbusrtu.read_3p3w_meter('/dev/ttyS1',3,1)
        #print(SubACLoop01)
        SubACLoop02 = FET_modbusrtu.read_3p3w_meter('/dev/ttyS1',4,1)
        #print(SubACLoop02)
        ACPayload = FET_modbusrtu.get_ACPayLoad(SubACLoop01,SubACLoop02)
        #print(ACPayload)
        MqttACSend(ACPayload)
        
        SubLoop01 = FET_modbustcp.getPowerLoop01('192.168.1.10',502,MainLoop01[0],MainLoop01[5])
        MqttSend(SubLoop01)
        SubLoop02 = FET_modbustcp.getPowerLoop02('192.168.1.11',502,MainLoop01[0],MainLoop01[5])
        MqttSend(SubLoop02)
        
        #Mainloop01Cal()
        #Mainloop02Cal()
        
        
        
        
               
        print('ok')
        return ('OK')
        
    except:
        print ('error')
        return ('error')

def IPC_Data():
    PowerPayload ={}
    clamp=[{"voltage":{}},{"voltage":{}},{"voltage":{}}]
    try:
        
        
        with open('static/data/PowerMainLoop01.json', 'r') as a:
            mainpower01 = json.load(a)
        a.close
        with open('static/data/PowerMainLoop02.json', 'r') as b:
            mainpower02 = json.load(b)
        b.close
        
        
        TotalMainPower = mainpower01["power"]+mainpower02["power"]
        clamp[0]["Main_Power"] = TotalMainPower
    
        PowerPayload[0] = [{"access_token": "nV5IbdeFN3I2Wjud96d8",
             "app": "ems_demo_fet",
             "type": "3P3WMETER",
             "data": [{"values":clamp[0]}]}]
    
        with open('static/data/ipc.json', 'w') as f:
            json.dump(PowerPayload[0][0]["data"][0]["values"], f)
        f.close
        
    except:
        pass

def Pub_infor():
    try:
        Mqttinfor = ReadMqttInfor()
        PowerInfor = PowerLoop()
        MainLoop01  = [
            {"access_token": PowerInfor["MainLoop01"]["access_token"],
             "app": PowerInfor["MainLoop01"]["app"],
             "type": PowerInfor["MainLoop01"]["type"],
             "data": PowerInfor["MainLoop01"]["data"]}]
        print (Mqttinfor['appInfo']['MQTT_UserName'])
    
        client = mqtt.Client('', True, None, mqtt.MQTTv31)
        client.username_pw_set(Mqttinfor['appInfo']['MQTT_UserName'], Mqttinfor['appInfo']['MQTT_Password'])
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client.tls_set_context(context)
        client.connect(Mqttinfor['appInfo']['MQTT_url'], Mqttinfor['appInfo']['MQTT_Port'], 60)
        client.loop_start()
        time.sleep(1)
        data02 = client.on_connect
        data03 = client.publish(Mqttinfor['appInfo']['MQTT_topic'],json.dumps(MainLoop01))
        time.sleep(3)
        client.loop_stop()
        client.disconnect()
        time.sleep(10)
        return ('OK')
    except:
        return ('error')
        
if __name__ == '__main__':
    while True:
        #PowerLoop()
        MqttPublish()
        time.sleep(60)