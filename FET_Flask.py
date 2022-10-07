from flask import Flask, render_template, request, jsonify, json

app = Flask(__name__)


@app.route('/setup')
def webapi():
    return render_template('setup.html')


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

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)