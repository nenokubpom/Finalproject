from flask import Flask, request, jsonify,render_template,blueprints
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import json
import connectjson
from flask_basicauth import BasicAuth
import os
import io
import base64
from ml_model import TFModel
from PIL import Image
from blueprints.home import home
from blueprints.allband import allbands
from blueprints.fromyear import fromyear
from blueprints.machine import machine





app = Flask(__name__)


app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.wsgi_app = ProxyFix(app.wsgi_app)
basic_auth = BasicAuth(app)
model = TFModel(model_dir='./ml-model/')
model.load()

api = Api(app, version='1.0', title='Girlgroup Kpop',
          description='Data of girl group',
          )

ns = api.namespace('girlgroup', description='Girlgroup profile')

task_model = api.model('Task', {
    'Name': fields.String(required=True, description='The task details')
})

peoplemod = api.model('Single', {
    'Name': fields.String(readonly=True, description='Name of single'),
    'Fullname': fields.String(required=True, description='Full name of single'),
    'Nationality':fields.String(required=True, description='Nationality of single'),
    'Day':fields.Integer(required=True, description='Day of birth'),
    'Month':fields.String(required=True, description='Month of birth'),
    'Year':fields.Integer(required=True, description='Year of birth'),
    'Band':fields.String(required=True, description='Band of single'),
    'Position':fields.String(required=True, description='Position in band'),
    'Height':fields.String(required=True, description='Height of single'),
    'IG':fields.String(required=True, description='Instragram of single'),
})

peoplemod2 = api.model('Single', {
    'Your':fields.String(readonly=True, description='Your answer'),
    'Name': fields.String(readonly=True, description='Name of single'),
    'Fullname': fields.String(required=True, description='Full name of single'),
    'Nationality':fields.String(required=True, description='Nationality of single'),
    'Day':fields.Integer(required=True, description='Day of birth'),
    'Month':fields.String(required=True, description='Month of birth'),
    'Year':fields.Integer(required=True, description='Year of birth'),
    'Band':fields.String(required=True, description='Band of single'),
    'Position':fields.String(required=True, description='Position in band'),
    'Height':fields.String(required=True, description='Height of single'),
    'IG':fields.String(required=True, description='Instragram of single'),
})

messagemod = api.model('message', {
    'Message': fields.String(readonly=True, description='Response of delete put or post request'),
    })

data = connectjson.show()

@ns.route('/')
class allgroup(Resource):
    @ns.doc('list_tasks')
    @ns.marshal_list_with(peoplemod)
    def get(self):
        return jsonify(data)
    
    @ns.doc('list_tasks')
    @ns.marshal_list_with(messagemod)
    def post(self):
        list = api.payload

        ret = []
        if len(list) == 3:
             quest = connectjson.add(list)
             if(quest == 200):
                ret = {"Message":"Request complete"}
        else:
            ret = {"Message":"Request failed"}
        return ret

    @basic_auth.required
    @ns.doc('list_tasks')
    @ns.marshal_list_with(messagemod)
    def put(self):
        name = api.payload
        ret = []
        quest = connectjson.updatedata(name)
        if(quest == 200):
            ret = {"Message":"Update complete"}
        else:
            ret = {"Message":"Update failed"}
        return ret

    @ns.doc('list_tasks')
    @ns.marshal_list_with(messagemod)
    @basic_auth.required
    def delete(self):
        name = api.payload['name']
        ret = []
        quest = connectjson.deletereq(name)
        if(quest == 200):
            ret = {"Message":"Delete complete"}
        else:
            ret = {"Message":"Delete failed"}
        return ret


@ns.route('/searchyear/<int:year>')
class memberfromyear(Resource):
    @ns.doc('list_tasks')
    @ns.marshal_list_with(peoplemod)
    def get(self,year):
        member = []
        for i in data:
            if int(i["Year"])<int(year):
                member.append({"Name": i["Name"],
    "Fullname": i["Fullname"],
    "Nationality": i["Nationality"],
    "Day": i["Day"],
    "Month": i["Month"],
    "Year": i["Year"],
    "Band": i["Band"],
    "Position": i["Position"],
    "Height": i["Height"],
    "IG": i["IG"]})
        return member


@ns.route('/<string:name>')
class name(Resource):
    @ns.doc('list_tasks')
    @ns.marshal_list_with(peoplemod)
    def get(self,name):
        member = []
        for i in data:
            if i["Name"].upper() == name.upper():
                member.append({"Name": i["Name"],
    "Fullname": i["Fullname"],
    "Nationality": i["Nationality"],
    "Day": i["Day"],
    "Month": i["Month"],
    "Year": i["Year"],
    "Band": i["Band"],
    "Position": i["Position"],
    "Height": i["Height"],
    "IG": i["IG"]})
        if member == []:
            member ={"Sorry":"Don't have her data"}
        return member

@ns.route('/band/<string:band>')
class band(Resource):
    @ns.doc('list_tasks')
    @ns.marshal_list_with(peoplemod)
    def get(self,band):
        member = []
        for i in data:
            if i["Band"].upper() == band.upper():
                member.append({"Name": i["Name"],
    "Fullname": i["Fullname"],
    "Nationality": i["Nationality"],
    "Day": i["Day"],
    "Month": i["Month"],
    "Year": i["Year"],
    "Band": i["Band"],
    "Position": i["Position"],
    "Height": i["Height"],
    "IG": i["IG"]})
        if member == []:
            member ={"Sorry":"Don't have band data"}
        return member

@ns.route('/game')
class game(Resource):

    @ns.doc('list_tasks')
    @ns.marshal_list_with(peoplemod2)
    def post(self):

        img_string = api.payload['base64']
        imgdata = base64.b64decode(img_string)
 
        image_temp = Image.open(io.BytesIO(imgdata))

        outputs = model.predict(image_temp)


        member = []

        for i in data:
            if i['Name'].upper()==outputs['predictions'][0]['label'].upper(): 
                member.append({"Your":"This is your in kpop girlgroup"
                    ,"Name": i["Name"],
    "Fullname": i["Fullname"],
    "Nationality": i["Nationality"],
    "Day": i["Day"],
    "Month": i["Month"],
    "Year": i["Year"],
    "Band": i["Band"],
    "Position": i["Position"],
    "Height": i["Height"],
    "IG": i["IG"]})
        return member

app.register_blueprint(home)
app.register_blueprint(allbands)
app.register_blueprint(fromyear)
app.register_blueprint(machine)
