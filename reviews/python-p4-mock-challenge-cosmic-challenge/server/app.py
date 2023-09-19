#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
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


@app.route('/')
def home():
    return ''

@app.route( '/planets', methods = ["GET"] )
def planets () :
    return make_response( Planet.all(), 200 )

@app.route( '/missions', methods = ['POST'] )
def missions () :
    try :
        data = request.get_json()
        new_mission = Mission(
            name = data[ 'name' ],
            scientist_id = data[ 'scientist_id' ],
            planet_id = data[ 'planet_id' ]
        )

        if new_mission.validation_errors :
            raise ValueError
        
        db.session.add( new_mission )
        db.session.commit()
        return make_response( new_mission.to_dict_with_ps(), 201 )

    except :
        errors = new_mission.validation_errors
        new_mission.clear_validation_errors()
        return make_response( { "errors": errors }, 422 )


@app.route( '/scientists', methods = ['GET', 'POST'] )
def scientists ( ) :
    if request.method == 'GET' :
        return make_response( Scientist.all(), 200 )
    
    elif request.method == 'POST' :
        data = request.get_json()
        new_scientist = Scientist(
            name = data[ 'name' ],
            field_of_study = data[ 'field_of_study' ]
        )

        errors = new_scientist.validation_errors
        if errors :
            new_scientist.clear_validation_errors()
            return make_response( { 'errors': errors }, 422 )
        else :
            db.session.add( new_scientist )
            db.session.commit()
            return make_response( new_scientist.to_dict(), 201 )


@app.route( '/scientists/<int:id>', methods = ['GET', 'PATCH', 'DELETE'] )
def scientist ( id ) :
    scientist = Scientist.find_by_id( id )
    if scientist :
        if request.method == 'GET' :
            scientist_dict = scientist.to_dict()
            scientist_dict[ 'missions' ] = [ mission.to_dict() for mission in scientist.missions ]
            return make_response( scientist_dict, 200 )
        
        elif request.method == 'PATCH' :
            try:
                data = request.get_json()
                for key in data :
                    setattr( scientist, key, data[ key ] )
                
                if scientist.validation_errors :
                    raise ValueError
                
                db.session.add( scientist )
                db.session.commit()
                return make_response( scientist.to_dict(), 200 )
            except :
                errors = scientist.validation_errors
                scientist.clear_validation_errors()
                return make_response( { 'errors':errors  }, 422 )
            
        elif request.method == 'DELETE' :
            for mission in scientist.missions : 
                db.session.delete( mission )
            db.session.delete( scientist )
            db.session.commit()

            return make_response( {}, 204 )

    else :
        return make_response( { 'error': 'Scientist not found.' }, 404 )


if __name__ == '__main__':
    app.run(port=5555, debug=True)
