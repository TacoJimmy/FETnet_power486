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
def MqttPublish():
    try:
        #PowerInfor = PowerLoop()
        
        MainLoop01 = FET_modbusrtu.read_Main_PowerMeter('/dev/ttyS1',1,1)
        print(MainLoop01)
        MainLoop02 = FET_modbusrtu.read_Main_PowerMeter('/dev/ttyS1',2,1)
        print(MainLoop02)
        #SubLoop01 = FET_modbustcp.getPowerLoop01('192.168.1.10',502,MainLoop01[0],MainLoop01[5])
        #MqttSend(SubLoop01)
        #SubLoop02 = FET_modbustcp.getPowerLoop02('192.168.1.11',502,MainLoop01[0],MainLoop01[5])
        #MqttSend(SubLoop02)
                
        print('ok')
        return ('OK')
        
    except:
        print ('error')
        return ('error')

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
        time.sleep(10)