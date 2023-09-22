#!/usr/bin/env python3
# 📚 Review With Students:
    # Authentication vs Authorization
    # Cookies vs Sessions
    # Using Bcrypt to hash and secure passwords
    # How Flask Encrypts Sessions

# Set up:
    # cd into server and run the following in the Terminal:
        # flask db init
        # flask db revision --autogenerate -m 'Create tables' 
        # flask db upgrade 
        # python seed.py
        # cd into client and run `npm i`

# Status codes
    # Most common response codes
        # 200 = ok ( GET, PATCH )
        # 201 = created ( POST )
        # 204 = no content ( DELETE )
        # 404 = not found
        # 401 = unauthorized ( Login )
        # 422 = unprocessable entity ( Validation Errors )
        # 418 = I'm a teapot! 🫖

# Let's start by moving most of our imports and other things into a new file called config.py
    # This will allow us to leave our app file focus just on routing and reduce clutter! Let's move lines 28-55!!! 🫡
from flask import Flask, request, make_response, abort, session, jsonify
from flask_migrate import Migrate

from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, Unauthorized

from flask_cors import CORS

# Import Bcrypt from flask_bcrypt
    # Make a variable called bcrypt set it equal to Bcrypt with app passed to it


from models import db, Production, CastMember, User

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up:
    # generate a secrete key `python -c 'import os; print(os.urandom(16))'`
app.secret_key = 'Secret Key Here!'

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Before starting here, let's make sure our models are in order!!! 🌟

# 1.✅ Create a Signup route
    #1.1 Use add_resource to add a new endpoint '/signup' 
    #1.2 The signup route should have a post method
        #1.2.1 Get the values from the request body with get_json
        #1.2.2 Create a new user, however only pass email/username ( and any other values we may have )
        #1.2.3 Call the password_hash method on the new user and set it to the password from the request
        #1.2.4 Add and commit
        #1.2.5 Add the user id to session under the key of user_id
        #1.2.6 send the new user back to the client with a status of 201
    #1.3 Test out your route with the client or Postman

# 2.✅ Test this route in the client/src/components/Authentication.sj 

# 3.✅ Create a Login route
    # 3.1 Create a login class that inherits from Resource
    # 3.2 Use api.add_resource to add the '/login' path
    # 3.3 Build out the post method
        # 3.3.1 convert the request from json and select the user sent form the client. 
        # 3.3.2 Use the email/username to query the user with a .filter
            # If the user exists check to make sure they have the correct password using user.authenticate
        # 3.3.3 If found and password is correct set the user_id to the session hash
        # 3.3.4 convert the user to_dict and send a response back to the client 
    #3.4 Toggle the signup form to login and test the login route


# 4.✅ Create an AuthorizedSession class that inherits from Resource
    # 4.1 use api.add_resource to add an authorized route
    # 4.2 Create a get method
        # 4.2.1 Access the user_id from session with session.get
        # 4.2.2 Use the user id to query the user with a .filter
        # 4.2.3 If the user id is in sessions and found make a response to send to the client. else raise the Unauthorized exception

# 5.✅ Head back to client/src/App.js to restrict access to our app!

# 6.✅ Logout 
    # 6.1 Create a class Logout that inherits from Resource 
    # 6.2 Create a method called delete
    # 6.3 Clear the user id in session by setting the key to None
    # 6.4 create a 204 no content response to send back to the client

# 7.✅ Navigate to client/src/components/Navigation.js to build the logout button!


class Productions(Resource):
    def get(self):
        return Production.all(), 200

    def post(self):
        rq = request.get_json()
        try :
            new_prod = Production(
                title=rq['title'],
                genre=rq['genre'],
                budget=int(rq['budget']),
                image=rq['image'],
                director=rq['director'],
                description=rq['description']
            )
        
            if new_prod.validation_errors :
                raise ValueError
            
            db.session.add( new_prod )
            db.session.commit()
            return new_prod.to_dict(), 201
        
        except :
            errors = new_prod.validation_errors
            new_prod.clear_validation_errors()
            return { 'errors': errors }, 422

api.add_resource(Productions, '/productions')


class ProductionByID(Resource):
    def get(self,id):
        prod = Production.find_by_id( id )
        if prod:
            return prod.to_dict(), 200
        else :
            return { 'errors': ['Production not found.'] }, 404

    def patch(self, id):
        prod = Production.find_by_id( id )
        if prod:
            try: 
                for attr in request.form:
                    setattr(prod, attr, request.form[attr])

                prod.ongoing = bool(request.form['ongoing'])
                prod.budget = int(request.form['budget'])

                if prod.validation_errors :
                    raise ValueError
                
                db.session.add( prod )
                db.session.commit()
                return prod.to_dict(), 200
            
            except :
                errors = prod.validation_errors
                prod.clear_validation_errors()
                return { 'errors': errors }, 422
        else :
            return { 'errors': ['Production not found.'] }, 404

    def delete(self, id):
        prod = Production.find_by_id( id )
        if prod :
            for cm in prod.cast :
                db.session.delete( cm )
            db.session.delete( prod )
            db.session.commit()
            return {}, 204
        else :
            return { 'errors': ['Production not found.'] }, 404

api.add_resource(ProductionByID, '/productions/<int:id>')


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: Sorry the resource you are looking for does not exist",
        404
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)