from flask import Flask, request, jsonify, redirect, render_template
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import os, random, secrets

app = Flask(__name__)

HIDDEN_URL = "https://chat.whatsapp.com/FKh5G5avaXf47ljKhTYFoF"
ADMIN_PIN = os.environ['ADMIN_PIN']
TIME_FORMAT = '%H:%M:%S'
SUBDOMAIN = os.environ['SUBDOMAIN']
SECRET_KEY = secrets.token_urlsafe(16)  


## Admin Panel
@app.route('/admin/<pin>')
def admin(pin):
    if (int(pin) != ADMIN_PIN):
        return jsonify({
            "err" : "access denied",
            "success" : False
        })
    else:
        return render_template('admin.html')

## Get encoded URL
@app.route('/api/getLink/', methods=['GET','POST'])
def getLink():
    secretPin = random.randint(999, 9999)
    s = Serializer(SECRET_KEY, 60*30) # 60 secs by 30 mins
    token = s.dumps({'secretPin': secretPin}).decode('utf-8') # encode user id 

    return jsonify({
        "url" : SUBDOMAIN + "/joinGC?token=" + str(token),
        "success" : True,
        "pin" : secretPin
    })

## Route for accessing url
@app.route('/joinGC/', methods=['GET'])
def joinGC():
    return render_template('join.html')

@app.route('/api/verify/', methods=['GET','POST'])
def verifyUser():
    ## Verify token
    res = {
        'token' : request.form['token'],
        'pin' : request.form['pin']
    }
    s = Serializer(SECRET_KEY)
    try: 
        secretPin = s.loads(res['token'])['secretPin']
    except:
        return None

    
    if (str(secretPin) == str(res['pin'])):
        return jsonify({
            "success" : True,
            "url" : HIDDEN_URL
        })

    else:
        return jsonify({
            "success" : False,
        })

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5053
    )
