    
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time

def publish_mqtt():
    meter_token = 'smartbuilding_device'
    FETnet_passwd = '?3NXw+Pp'

    data01  = [
        {"access_token": "WImETF1BotX8l1xIkZ3K",
         "app": "ems_demo_fet",
         "ts": 1665172851000,
         "type": "METER",
         "data": [{"values": {"bb": "22","demand": "50","voltage": "380","power": "300","current_r": "20","current_s": "20","current_t": "20"}}]}]
    try:
        client = mqtt.Client('', True, None, mqtt.MQTTv31)
        client.username_pw_set(meter_token, FETnet_passwd)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client.tls_set_context(context)
        client.connect("mqttd.fetnet.net", 8883, 60)
        client.loop_start()
        time.sleep(1)
        client.on_connect
        client.publish('/ems/v1/telemetry/demoNH468',json.dumps(data01))
        time.sleep(3)
        client.loop_stop()
        client.disconnect()
    except:
        print ("error")
        #return ('loss_connect')

while True:
    publish_mqtt
    time.sleep(6000)