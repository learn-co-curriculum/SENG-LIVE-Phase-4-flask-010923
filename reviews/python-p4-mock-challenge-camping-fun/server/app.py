#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

validation_errors = {"errors": ["validation errors"]}

class Campers(Resource):
    def get(self):
        campers = Camper.query.all()
        # campers_dict = [camper.to_dict(only = ("id", "name", "age")) for camper in campers]
        campers_dict = [camper.to_dict(rules = ("-signups",)) for camper in campers]

        return make_response(campers_dict, 200)
    
    def post(self):
        rq = request.get_json()
        try:

            camper = Camper(
                name = rq.get("name"),
                age = rq.get("age")
            )

            db.session.add(camper)
            db.session.commit()
            camper_json = camper.to_dict(rules = ("-signups",))
            return make_response(camper_json, 201)
        except:
            return make_response(validation_errors, 400)

class Campers_By_Id(Resource):
    def get(self, id):
        camper = Camper.query.get(id)

        if camper:
            camper_json = camper.to_dict()
            return make_response(camper_json, 200)
        else:
            return make_response({"error":"Camper not found"}, 404)
    
    def patch(self, id):
        camper = Camper.query.get(id)
        rq = request.get_json()

        if camper:
            try:
                for attr in rq:
                    setattr(camper, attr, rq.get(attr))

                db.session.commit()
                camper_json = camper.to_dict(rules = ("-signups",))
                return make_response(camper_json, 202)
            except:
                return make_response(validation_errors, 400)
        else:
            return make_response({"error":"Camper not found"}, 404)
    

class Activities(Resource):
    def get(self):
        activities = Activity.query.all()
        activities_dict = [activity.to_dict(rules = ("-signups",)) for activity in activities]

        return make_response(activities_dict, 200)

class Activities_By_Id(Resource):
    def delete(self, id):
        activity = Activity.query.get(id)

        if activity:
            db.session.delete(activity)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Activity not found"}, 404)

class Signups(Resource):
    def post(self):
        rq = request.get_json()
        try:
            signup = Signup(
                camper_id = rq.get("camper_id"),
                activity_id = rq.get("activity_id"),
                time = rq.get("time")
            )
            db.session.add(signup)
            db.session.commit()
            signup_json = signup.to_dict()
            return make_response(signup_json, 201)
        except:
            return make_response(validation_errors, 400)


api.add_resource(Campers, "/campers")
api.add_resource(Campers_By_Id, "/campers/<int:id>")
api.add_resource(Activities, "/activities")
api.add_resource(Activities_By_Id, "/activities/<int:id>")
api.add_resource(Signups, "/signups")




# @app.route('/')
# def home():
#     return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
