from flask import Flask, render_template, request, jsonify, json
import schedule  
import time  
from flask import Flask
from flask_apscheduler import APScheduler
import FET_MQTT
import FET_modbusrtu
import FET_modbustcp
app = Flask(__name__)

class Config(object):
    JOBS = [
        {
            'id': 'publish_PowerMeter',  
            'func': '__main__:publish_PowerMeter',
            'args': (1, 2),   
            'trigger': 'interval',
            'minutes': 1 
        },
        {
            'id': 'read_com1',  
            'func': '__main__:read_com1',
            'args': (1, 2),   
            'trigger': 'interval',
            'seconds': 15 
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

@app.route('/powermanage/ipc', methods=['GET'])
def poweripc():
    if request.method == "GET":
        with open('static/data/jpc.json', 'r') as f:
            data = json.load(f)
            print("text : ", data)
        f.close
        return jsonify(data)

@app.route('/powermanage/mainloop01', methods=['GET'])
def powermainloop01():
    if request.method == "GET":
        with open('static/data/PowerMainLoop01.json', 'r') as f:
            data = json.load(f)
            #print("text : ", data)
        f.close
        return jsonify(data)
    
@app.route('/powermanage/mainloop02', methods=['GET'])
def powermainloop02():
    if request.method == "GET":
        with open('static/data/PowerMainLoop02.json', 'r') as f:
            data = json.load(f)
            #print("text : ", data)
        f.close
        return jsonify(data)
    
@app.route('/powermanage/subloop01', methods=['GET'])
def powersubloop01Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop01.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop02', methods=['GET'])
def powersubloop02Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop02.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop03', methods=['GET'])
def powersubloop03Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop03.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop04', methods=['GET'])
def powersubloop04Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop04.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop05', methods=['GET'])
def powersubloop05Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop05.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop06', methods=['GET'])
def powersubloop06Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop06.json', 'r') as f:
            data = json.load(f)
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

@app.route('/powermanage/subloop09', methods=['GET'])
def powersubloop09Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop09.json', 'r') as f:
            data = json.load(f)
        f.close
    return jsonify(data)
@app.route('/powermanage/subloop10', methods=['GET'])
def powersubloop10Message():
    if request.method == "GET":
        with open('static/data/PowerSubLoop10.json', 'r') as f:
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
    try:
        FET_modbustcp.power_count()   
    except:
        pass
    
    
if __name__ == '__main__':
    
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app) 
    scheduler.start()    
    app.run('0.0.0.0', debug=True)