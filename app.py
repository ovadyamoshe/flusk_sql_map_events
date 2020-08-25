from flask import Flask, request, jsonify, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)

# home page
@app.route('/',methods=['GET','POST'])
def my_maps():

    mapbox_access_token = 'pk.eyJ1Ijoib3ZhZHlhbW9zaGUiLCJhIjoiY2tlNTVkbWdvMDdvOTJ5cG9qeDdweHl3eCJ9.pvdg3-74CpirjfzfO3lMCw'

    return render_template('index.html',
        mapbox_access_token=mapbox_access_token)

@app.route('/Test2',methods=['GET','POST'])
def test():

    mapbox_access_token = 'pk.eyJ1Ijoib3ZhZHlhbW9zaGUiLCJhIjoiY2tlNTVkbWdvMDdvOTJ5cG9qeDdweHl3eCJ9.pvdg3-74CpirjfzfO3lMCw'

    return render_template('test2.html',
        mapbox_access_token=mapbox_access_token)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# event Class/Model
class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String(200))
  event_type = db.Column(db.String(100))
  Coordinate = db.Column(db.String(250))


  def __init__(self, name, description, event_type, Coordinate):
    self.name = name
    self.description = description
    self.event_type = event_type
    self.Coordinate = Coordinate


# event Schema
class EventSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'event_type', 'Coordinate')

# Init schema
event_schema = EventSchema()
events_schema = EventSchema(many=True)

# Create a event
@app.route('/event', methods=['POST'])
def add_event():
  name = request.json['name']
  description = request.json['description']
  event_type = request.json['event_type']
  Coordinate = request.json['Coordinate']
  new_event = Event(name, description, event_type, Coordinate)
  db.session.add(new_event)
  db.session.commit()

  return event_schema.jsonify(new_event)


# Get All Events
@app.route('/event', methods=['GET'])
def get_events():
  all_events = Event.query.all()
  result = events_schema.dump(all_events)
  return jsonify(result)

# Get Single Event
@app.route('/event/<id>', methods=['GET'])
def get_event(id):
  event = Event.query.get(id)
  return event_schema.jsonify(event)

# Update a Event
@app.route('/event/<id>', methods=['PUT'])
def update_event(id):
  event = Event.query.get(id)

  name = request.json['name']
  description = request.json['description']
  event_type = request.json['event_type']
  Coordinate = request.json['Coordinate']

  event.name = name
  event.description = description
  event.event_type = event_type


  db.session.commit()

  return event_schema.jsonify(event)

# Delete Event
@app.route('/event/<id>', methods=['DELETE'])
def delete_event(id):
  event = Event.query.get(id)
  db.session.delete(event)
  db.session.commit()

  return event_schema.jsonify(event)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)