#!/usr/bin/env python3
# 📚 Review With Students:
# Set up:
    # cd into server and run the following in Terminal:
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5000
        # flask db init
        # flask db revision --autogenerate -m'Create tables' 
        # flask db upgrade 
        # python seed.py
# Running React Together 
     # In Terminal, run:
        # `honcho start -f Procfile.dev`

from flask import Flask, request, make_response, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, Unauthorized
from flask_cors import CORS

# 1.✅ Import Bcrypt form flask_bcrypt
    #1.1 Invoke Bcrypt and pass it app

# 2.✅ Navigate to "models.py"
    # Continue on Step 3

from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app) 
bcrypt = Bcrypt(app)
from models import db, Production, CrewMember, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

app.secret_key = b'@~xH\xf2\x10k\x07hp\x85\xa6N\xde\xd4\xcd'


migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Productions(Resource):
    def get(self):
        production_list = [p.to_dict() for p in Production.query.all()]
        response = make_response(
            production_list,
            200,
        )

        return response

    def post(self):
        form_json = request.get_json()
        new_production = Production(
            title=form_json['title'],
            genre=form_json['genre'],
            budget=int(form_json['budget']),
            image=form_json['image'],
            director=form_json['director'],
            description=form_json['description']
        )

        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        response = make_response(
            response_dict,
            201,
        )
        return response
api.add_resource(Productions, '/productions')


class ProductionByID(Resource):
    def get(self,id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            raise NotFound
        production_dict = production.to_dict()
        response = make_response(
            production_dict,
            200
        )
        
        return response

    def patch(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            raise NotFound

        for attr in request.form:
            setattr(production, attr, request.form[attr])

        production.ongoing = bool(request.form['ongoing'])
        production.budget = int(request.form['budget'])

        db.session.add(production)
        db.session.commit()

        production_dict = production.to_dict()
        
        response = make_response(
            production_dict,
            200
        )
        return response

    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            raise NotFound
        db.session.delete(production)
        db.session.commit()

        response = make_response('', 204)
        
        return response
api.add_resource(ProductionByID, '/productions/<int:id>')

# 8.✅ Create a Signup route
    #8.1 Use add_resource to add a new endpoint '/signup' 
    #8.2 The signup route should have a post method
        #8.2.1 Get the values from the request body with get_json
        #8.2.2 Create a new user, however only pass in the name, email and admin values
        #8.2.3 Call the password_hash method on the new user and set it to the password from the request
        #8.2.4 Add and commit
        #8.2.5 Add the user id to session under the key of user_id
        #8.2.6 send the new user back to the client with a status of 201
    #8.3 Test out your route with the client or Postman
    
class Signup(Resource):
     def post(self):
        
        name = request.get_json()['name']
        email = request.get_json()['name']
        password = request.get_json()['password']

        new_user = User(name=name, email=email, admin=False)
        new_user.password_hash = password
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
                
        return new_user.to_dict(), 201

api.add_resource(Signup, '/signup', endpoint='signup')

# 9.✅ Create a Login route
    #9.1 Use add add_resource to add the login endpoint
    #9.2 Create a post method
        #9.2.1 Query the user from the DB with the name provided in the request
        #9.2.2 Set the user's id to sessions under the user_id key
        #9.2.3 Create a response to the client with the user's data
class Login(Resource):

    def post(self):
        user = User.query.filter(User.name == request.get_json()['name']).first()
        session['user_id'] = user.id
        user_dict = user.to_dict()
        response = make_response(
            user_dict,
            200,
        )
        return response

api.add_resource(Login, '/login', endpoint='login')

# 10.✅ Create a route that checks to see if the user is currently in sessions
    # 10.1 Use add_resource to add an authorized endpoint
    # 10.2 Create a Get method
        #10.2.1 Check to see if the user_id is in session
        #10.2.2 If found query the user and send it to the client
        #10.2.3 If not found return a 401 Unauthorized error
class AuthorizedSession(Resource):
    def get(self):

        if session.get('user_id'):
            
            user = User.query.filter(User.id == session['user_id']).first()
            
            return user.to_dict(), 200
            
        else:
            raise Unauthorized


api.add_resource(AuthorizedSession, '/authorized', endpoint='authorized')

# 11.✅ Create a logout route
    #11.1 use add_resource to add a logout endpoint
    #11.2 Create a delete method
        #11.2.1 Set the user_id in sessions to None
        #11.2.1 Create a response with no content and a 204
    #11.3 Test out your route with the client or Postman

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        response = make_response('',204,)
        return response

api.add_resource(Logout, '/logout', endpoint='logout')


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: Sorry the resource you are looking for does not exist",
        404
    )

    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)