#!/usr/bin/env python3

# 📚 Review With Students:
    # CORS
    # Error handling

# Status codes
    # Most common response codes
        # 200 = ok
        # 201 = created ( post )
        # 204 = no content ( delete )
        # 404 = not found
        # 401 = unauthorized ( login )
        # 422 = unprocessable entity ( validation errors )
        # 418 = I'm a teapot! 🫖

# Set up:
    # cd into server and run the following in Terminal
        # flask db init
        # flask db revision --autogenerate -m'Create tables' 
        # flask db upgrade 
        # python seed.py
        # flask shell
        # Run the server with 'python app.py'

        # ( Optional ) If you want to use the 'flask run' command do these first:
            # export FLASK_APP=app.py
            # export FLASK_RUN_PORT=5555
            # export FLASK_DEBUG=1

# Running React Together 

from flask import Flask, request, make_response, abort, jsonify
from flask_migrate import Migrate

from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

# 1.✅ Import CORS from flask_cors, invoke it and pass it app
from flask_cors import CORS


# 2.✅ Create validations for the Production model

# 3.✅ Start up the server / client and navigate to client/src/App.js

from models import db, Production, CastMember

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
CORS( app )

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: Sorry the resource you are looking for does not exist",
        404
    )
    return response


class Productions ( Resource ) :
    def get ( self ) :
        return make_response( Production.all(), 200 )
    
    def post ( self ) :
        rq = request.get_json()
        new_prod = Production(
            title = rq[ 'title' ],
            budget = rq[ 'budget' ],
            genre = rq[ 'genre' ],
            image = rq[ 'image' ],
            director = rq[ 'director' ],
            description = rq[ 'description' ]
        )

        errors = new_prod.validation_errors
        if errors :
            new_prod.clear_validation_errors()
            return make_response( { 'errors': errors }, 422 )
        else :
            db.session.add( new_prod )
            db.session.commit()
            return make_response( new_prod.to_dict_with_cast(), 201 )
        

api.add_resource( Productions, '/productions', endpoint = 'productions' )

class ProductionById ( Resource ) :
    def get ( self, id ) :
        prod = Production.find_by_id( id )
        if prod :
            return make_response( prod.to_dict_with_cast(), 200 )
        else :
            return make_response( { 'errors': ['Production was not found.'] }, 404 )
        
    def patch ( self, id ) :
        prod = Production.find_by_id( id )
        if prod :
            rq = request.get_json()
            for attr in rq :
                setattr( prod, attr, rq[ attr ] )

            new_prod = Production(
                title = prod[ 'title' ],
                budget = prod[ 'budget' ],
                genre = prod[ 'genre' ],
                image = prod[ 'image' ],
                director = prod[ 'director' ],
                description = prod[ 'description' ]
            )
            
            errors = new_prod.validation_errors
            if errors :
                new_prod.clear_validation_errors()
                return make_response( { 'errors': errors }, 422 )
            else :
                db.session.add( prod )
                db.session.commit()
                return make_response( prod.to_dict_with_cast(), 200 )
        else :
            return make_response( { 'errors': ['Production was not found.'] }, 404 )
        
    def delete ( self, id ) :
        prod = Production.find_by_id( id )
        if prod :
            for cm in prod.cast_members :
                db.session.delete( cm )
            db.session.delete( prod )
            db.session.commit()
            return make_response( {}, 204 )

api.add_resource( ProductionById, '/productions/<int:id>', endpoint = 'production' )


@app.route( '/cast_members', methods = [ 'GET', 'POST' ] )
def cast_members ( ) :
    if request.method == 'GET' :
        return make_response( CastMember.all(), 200 )
    
    elif request.method == 'POST' :
        rq = request.get_json()
        new_cm = CastMember(
            name = rq[ 'name' ],
            role = rq[ 'role' ],
            # A cast member should be part of a production!!!
            production_id = rq[ 'production_id' ]
        )
        errors = new_cm.validation_errors
        if errors :
            new_cm.clear_validation_errors()
            return make_response( { 'errors': errors }, 422 )
        else :
            db.session.add( new_cm )
            db.session.commit()
            return make_response( new_cm.to_dict() , 201 )


@app.route( '/cast_members/<int:id>', methods = [ 'GET', 'PATCH', 'DELETE' ] )
def cast_member ( id ) :
    cm = CastMember.find_by_id( id )
    if cm :
        if request.method == 'GET' :
            return make_response( cm.to_dict_with_prod(), 200 )
        elif request.method == 'DELETE' :
            db.session.delete( cm )
            db.session.commit()
            return make_response( {}, 204 )
        elif request.method == 'PATCH' :
            rq = request.get_json()

            new_cm = CastMember(
            name = rq[ 'name' ],
            role = rq[ 'role' ],
            production_id = rq[ 'production_id' ]
        )
        errors = new_cm.validation_errors
        if errors :
            new_cm.clear_validation_errors()
            return make_response( { 'errors': errors }, 422 )
        else :
            cm.name = rq[ 'name' ]
            cm.role = rq[ 'role' ]
            cm.production_id = rq[ 'production_id' ]
            db.session.add( cm )
            db.session.commit()
            return make_response( cm.to_dict_with_prod(), 200 )
    else :
        return make_response( { 'errors': ['Cast member was not found.'] }, 404 )

# To run the file as a script
if __name__ == '__main__':
    app.run(port=5555, debug=True)

#Sample Data for testing POST
# {
#     "title": "Macbeth",
#     "genre": "Drama",
#     "description": "3 witches told Macbeth he was I was going to be the king of Scotland and some bad stuff happened",
#     "budget": 100000.0,
#     "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/First-page-first-folio-macbeth.jpg/369px-First-page-first-folio-macbeth.jpg",
#     "director": "Bill Shakespeare",
#     "ongoing": true
#     }