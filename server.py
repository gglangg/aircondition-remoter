from flask import Flask,request,render_template,jsonify
import datetime
import os
from time import sleep

def returnUpdateTime():

    now = datetime.datetime.now()

    return 'latest update {}'.format(now.strftime("%m-%d %H:%M:%S")) 


CMD = ''
PREFIX_CMD = "/usr/bin/irsend SEND_ONCE AIR_CONDITIONER "

def runCMD(cmd:str):
    global CMD
    CMD = cmd
    sleep(1)
    if CMD == cmd:
        os.system(cmd)
        CMD=''
    
TEMPERATURE = 25

MODE = '冷氣'

LATEST_UPDATE = returnUpdateTime()



app = Flask(__name__)

KEY = 'oqaijOQI'

@app.route('/')
def home():
    key = request.args.get('key', 0)
    if key==KEY:
        return render_template('template.html', key=KEY, msg=LATEST_UPDATE,mode=MODE,temperature=TEMPERATURE)
    return '<h1>Invalid Key</h1>'

@app.route('/run')
def about():

    global TEMPERATURE, MODE, LATEST_UPDATE
    
    key = request.args.get('key', 0)
    cmd = request.args.get('cmd', 0)

    if 'HEAT' in cmd:
        return render_template('template.html', key=KEY, msg=LATEST_UPDATE+' HEAT disable',mode=MODE,temperature=TEMPERATURE)

    if cmd=='POWER_OFF':
        LATEST_UPDATE = 'POWER_OFF'
        runCMD(PREFIX_CMD + cmd)
        # os.system( PREFIX_CMD + cmd)
        return render_template('template.html', key=KEY, msg=LATEST_UPDATE,mode=MODE,temperature=TEMPERATURE)
        

    TEMPERATURE = cmd.split('t')[-1]

    M = cmd.split('_')[0]
    if M=='COOL':
        MODE = '冷氣'
    elif M=='DRY':
        MODE = '除濕'
    elif M=='HEAT':
        MODE = '暖氣'

    if key==KEY:
        runCMD(PREFIX_CMD + cmd)
        # os.system( PREFIX_CMD + cmd)
        LATEST_UPDATE = returnUpdateTime()

        return render_template('template.html', key=KEY, msg=LATEST_UPDATE,mode=MODE,temperature=TEMPERATURE)



    return '<h1>Invalid Key</h1>'





@app.route('/update')
def update():
    global CMD
    if CMD=='':
        return None,404

    key = request.args.get('key', 0)

    if key==KEY:



        # LATEST_UPDATE = returnUpdateTime()

        data = {

            'msg': LATEST_UPDATE,

            'mode': MODE,

            'temperature': TEMPERATURE,

        }    

        return jsonify(data)



    

    return '<h1>Invalid Key</h1>'









if __name__ == '__main__':



    app.run(host='0.0.0.0', port=8080)


