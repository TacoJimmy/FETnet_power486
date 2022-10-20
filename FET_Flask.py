from flask import Flask, render_template, request, jsonify, json
import schedule  
import time  
from flask import Flask
from flask_apscheduler import APScheduler
import FET_MQTT
import FET_modbusrtu

app = Flask(__name__)

class Config(object):
    JOBS = [
        {
            'id': 'publish_PowerMeter',  
            'func': '__main__:publish_PowerMeter',
            'args': (1, 2),   
            'trigger': 'interval',
            'seconds': 60 
        },
        {
            'id': 'read_com1',  
            'func': '__main__:read_com1',
            'args': (1, 2),   
            'trigger': 'interval',
            'seconds': 10 
        }
    ]
    SCHEDULER_API_ENABLED = True

@app.route('/setup')
def webapi():
    return render_template('setup.html')


@app.route('/powermanage')
def powermanage():
    return render_template('powermanage.html')

@app.route('/powermanage/message', methods=['GET'])
def powermanageMessage():
    if request.method == "GET":
        with open('static/data/message.json', 'r') as f:
            data = json.load(f)
            print("text : ", data)
        f.close
        return jsonify(data)
@app.route('/powermanage/subloop07', methods=['GET'])
def powersubloop07Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop07.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop08', methods=['GET'])
def powersubloop08Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop08.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)


@app.route('/setup/message', methods=['GET'])
def getDataMessage():
    if request.method == "GET":
        with open('static/data/message.json', 'r') as f:
            data = json.load(f)
            print("text : ", data)
        f.close
        return jsonify(data)


@app.route('/setup/COM01', methods=['POST'])
def setDataCOM01():
    if request.method == "POST":
        data = {
            'appInfo': {
                'COM01_Status': request.form['COM01_Status'],
                'COM01_BaudRate': request.form['COM01_BaudRate'],
                'COM01_DataSize': request.form['COM01_DataSize'],
                'COM01_Parity': request.form['COM01_Parity'],
                'COM01_StopBits': request.form['COM01_StopBits'],
            }
        }
        print(type(data))
        with open('static/data/COM01.json', 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')
    
@app.route('/setup/COM02', methods=['POST'])
def setDataCOM02():
    if request.method == "POST":
        data = {
            'appInfo': {
                'COM02_Status': request.form['COM02_Status'],
                'COM02_BaudRate': request.form['COM02_BaudRate'],
                'COM02_DataSize': request.form['COM02_DataSize'],
                'COM02_Parity': request.form['COM02_Parity'],
                'COM02_StopBits': request.form['COM02_StopBits'],
            }
        }
        print(type(data))
        with open('static/data/COM02.json', 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')
    
@app.route('/setup/TCP01', methods=['POST'])
def setDataTCP01():
    if request.method == "POST":
        data = {
            'appInfo': {
                'TCP01_IP': request.form['TCP01_IP'],
                'TCP01_PORT': request.form['TCP01_PORT'],
            }
        }
        print(type(data))
        with open('static/data/TCP01.json', 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')

@app.route('/setup/TCP02', methods=['POST'])
def setDataTCP02():
    if request.method == "POST":
        data = {
            'appInfo': {
                'TCP02_IP': request.form['TCP02_IP'],
                'TCP02_PORT': request.form['TCP02_PORT'],
            }
        }
        print(type(data))
        with open('static/data/TCP02.json', 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')

@app.route('/setup/mqtt01', methods=['POST'])
def setDataMqtt01():
    if request.method == "POST":
        data = {
            'appInfo': {
                'MQTT_ClientID': request.form['MQTT_ClientID'],
                'MQTT_UserName': request.form['MQTT_UserName'],
                'MQTT_Password': request.form['MQTT_Password'],
                'MQTT_url': request.form['MQTT_url'],
                'MQTT_Port': request.form['MQTT_Port'],
                'MQTT_SSL': request.form['MQTT_SSL'],
            }
        }
        print(type(data))
        with open('static/data/mqtt01.json', 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')

def publish_PowerMeter(a, b):
    
    FET_MQTT.MqttPublish()
    
def read_com1(a, b):
    '''
    with open('static/data/COM01.json', 'r') as f:
        com1_infor = json.load(f)
    f.close
    if com1_infor["appInfo"]["COM01_Status"] == "Enable":
       modbus_data = FET_modbusrtu.getCom1_Power('COM3',int(com1_infor["appInfo"]["COM01_BaudRate"]),104,'INPUT')
       print (type(modbus_data))
       print (modbus_data)
       #print (FET_MQTT.Pub_infor())
    '''
    
if __name__ == '__main__':
    
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app) 
    scheduler.start()    
    app.run('0.0.0.0', debug=True)