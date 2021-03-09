# need to pip before import works
# need to pip before import works

import json;
from json import JSONEncoder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, jsonify, request, redirect, url_for

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:test1234@localhost/jad'
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    model = db.Column(db.String(20), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    color = db.Column(db.String(20), unique=False, nullable=False)

    def update(self,newdata):
        for key,value in newdata.items():
            setattr(self,key,value)  

    def serialize(self):
        return {
        'id':self.id,
        'name':self.name,
        'model':self.model,
        'year':self.year,
        'color':self.color
    }

db.create_all()

@app.route('/car', methods=['POST'])
def addCar():
    dc = json.loads(request.data)
    aa = Car(**dc)
    db.session.add(aa)                       
    db.session.commit()
    return redirect(url_for('getCar',id=aa.id))


@app.route('/cars', methods=['GET'])
def getCars():
    cars = Car.query.all()
    return jsonify(car= [c.serialize() for c in cars])


@app.route('/car/<int:id>', methods=['GET'])
def getCar(id):    
    c = Car.query.filter_by(id=id).one().id
    return jsonify(c.serialize())


@app.route('/car/<int:id>', methods=['PUT'])
def updateCar(id):    
    c = Car.query.filter_by(id=id).one()
    dc = json.loads(request.data)
    c.update(dc)
    db.session.commit()
    return jsonify(c.serialize())


@app.route('/car/<int:id>', methods=['DELETE'])
def deleteCar(id):    
    c = Car.query.filter_by(id=id).one()
    db.session.delete(c)
    db.session.commit()
    return jsonify("")

app.run()





