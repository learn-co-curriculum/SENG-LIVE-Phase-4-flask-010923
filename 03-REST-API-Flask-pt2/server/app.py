#!/usr/bin/env python3
# 📚 Review With Students:
    # REST
    # Status codes
        # Most common response codes
            # 200 = ok
            # 201 = created ( post )
            # 204 = no content ( delete )
            # 404 = not found
            # 401 = unauthorized ( login )
            # 422 = unprocessable entity ( validation errors )
    # Error handling 
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

# Stretch Goal: Talk about redirect

from flask import Flask, request, make_response, abort
from flask_migrate import Migrate

# ✅ Import `Api` and `Resource` from `flask_restful`
from flask_restful import Api, Resource
from flask_restful import Api, Resource

# 1.✅ Import NotFound from werkzeug.exceptions for error handling


from models import db, Production, CastMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


# 2.✅ use the @app.errorhandler() decorator to handle Not Found
    # 2.1 Create the decorator and pass it NotFound
    # 2.2 Use make_response to create a response with a message and the status 404
    # 2.3 return the response

class Productions ( Resource ) :
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

# 3.✅ If a production is not found raise the NotFound exception

# 4.✅ Patch
    # 4.1 Create a patch method that takes self and id
    # 4.2 Query the Production from the id
    # 4.3 If the production is not found raise the NotFound exception
    # 4.4 Loop through the request.form object and update the productions attributes. Note: Be cautions of the data types to avoid errors.
    # 4.5 add and commit the updated production 
    # 4.6 Create and return the response

# 5.✅ Delete
    # 5.1 Create a delete method, pass it self and the id
    # 5.2 Query the Production 
    # 5.3 If the production is not found raise the NotFound exception
    # 5.4 delete the production and commit 
    # 5.5 create a response with the status of 204 and return the response 



api.add_resource(ProductionByID, '/productions/<int:id>')

@app.route( '/cast_members', methods = [ 'GET', 'POST' ] )
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


@app.route( '/cast_members/<int:id>', methods = [ 'GET' ] )
def cast_member ( id ) :
    cm = CastMember.find_by_id( id )
    if cm :
        if request.method == 'GET' :
            return make_response( cm.to_dict_with_prod(), 200 )
    else :
        return make_response( { 'errors': ['Cast member was not found.'] }, 404 )


# To run the file as a script
if __name__ == '__main__':
    app.run(port=5555, debug=True)
