# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time

if __name__ == '__main__':
    while True:
        meter_token = 'smartbuilding_device'
        FETnet_passwd = '?3NXw+Pp'

    
        data01  = [
            {"access_token": "aqknLWRH5UD3sjMqnTOA",
             "app": "ems_demo_fet",
             "ts": 1663824407000,
             "type": "METER",
             "data": [{"values": {
                 "voltage": "22",
                 "current_r": "50",
                 "current_s": "380",
                 "current_t": "300",
                 "power": "20",
                 "pf": "20",
                 "energy": "20",
                 "temperature_r": "20",
                 "temperature_s": "23",
                 "temperature_t": "25",
                 "demand": "20",
                 "alive": "20",
                 "remark": "20",
        }}]}]
    
        client = mqtt.Client('', True, None, mqtt.MQTTv31)
        client.username_pw_set(meter_token, FETnet_passwd)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client.tls_set_context(context)
        client.connect("mqttd.fetnet.net", 8883, 60)
        client.loop_start()
        time.sleep(1)
        data02 = client.on_connect
        data03 = client.publish('/ems/v1/telemetry/demoNH220',json.dumps(data01))
        print(data02)
        print(data03)
        time.sleep(3)
        client.loop_stop()
        client.disconnect()
        time.sleep(10)

