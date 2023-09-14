#!/usr/bin/env python3

# 📚 Review With Students:
    # API Fundamentals
    # MVC Architecture and Patterns / Best Practices
    # RESTful Routing
    # Serialization
    # Postman/Thunder Client

# Set Up:
    # In Terminal, `cd` into `server` and run the following:
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5555
        # export FLASK_DEBUG=1
        # flask db init
        # flask db revision --autogenerate -m 'Create tables' 
        # flask db upgrade 
        # python seed.py
        # flask shell
    # Talk about debug + hot reload and flask shell
    # Stretch Goal: Talk about redirect

# Restful

# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|



from flask import Flask, request, make_response, jsonify, abort
from flask_migrate import Migrate

# 1. ✅ Import `Api` and `Resource` from `flask_restful`
from flask_restful import Api, Resource
    # ❓ What do these two classes do at a higher level? 

from models import db, Production, CastMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Note: `app.json.compact = False` configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api( app )

# 2. ✅ Initialize the Api
    # `api = Api(app)`

    # 2.1 Create routes for cast members without using Flask Rest API conventions
        # Show model helper methods

    # 2.2 Create a method to get all cast members
@app.route( '/cast_members', methods = [ 'GET', 'POST' ] )
    # 2.3✅ Talk about how to restrict which fetch methods are allowed
def cast_members ( ) :
    if request.method == 'GET' :
        return make_response( CastMember.all(), 200 )
    
    elif request.method == 'POST' :
        rq = request.get_json()
        new_cm = CastMember(
            name = rq[ 'name' ],
            role = rq[ 'role' ]
        )
        db.session.add( new_cm )
        db.session.commit()
        return make_response( new_cm.to_dict() , 201 )
    
    # 2.4 Create a method for getting a single cast member
@app.route( '/cast_members/<int:id>', methods = [ 'GET' ] )
def cast_member ( id ) :
    cm = CastMember.find_by_id( id )
    if cm :
        if request.method == 'GET' :
            return make_response( cm.to_dict_with_prod(), 200 )
    else :
        return make_response( { 'errors': ['Cast member was not found.'] }, 404 )
    # 2.5 Show off abort

    
    # 2.6 Talk about the most common response codes
    # 200 = ok
    # 201 = created ( post )
    # 204 = no content ( delete )
    # 404 = not found
    # 401 = unauthorized
    # 422 = unprocessible entity


# 3. ✅ Create a Production class that inherits from Resource
class Productions ( Resource ) :
# 4. ✅ Create a GET (All) Route
    def get ( self ) :
        return make_response( Production.all(), 200 )
    

api.add_resource( Productions, '/productions', endpoint = 'productions' )

class ProductionById ( Resource ) :
    def get ( self, id ) :
        prod = Production.find_by_id( id )
        if prod :
            return make_response( prod.to_dict_with_cast(), 200 )
        else :
            return make_response( { 'errors': ['Production was not found.'] }, 404 )

api.add_resource( ProductionById, '/productions/<int:id>', endpoint = 'production' )

if __name__ == '__main__':
    app.run(port=5555, debug=True)