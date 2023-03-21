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

app = Flask(__name__)
CORS(app) 

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

# 7.✅ Create a Signup route
    #7.1 Use add_resource to add a new endpoint '/signup' 
    #7.2 The signup route should have a post method
        #7.2.1 Get the values from the request body with get_json
        #7.2.2 Create a new user, however only pass in the name, email and admin values
        #7.2.3 Call the password_hash method on the new user and set it to the password from the request
        #7.2.4 Add and commit
        #7.2.5 Add the user id to session under the key of user_id
        #7.2.6 send the new user back to the client with a status of 201
    #7.3 Test out your route with the client or Postman


# 8.✅ Create a Login route
    #8.1 use add add_resource to add the login endpoint
    #8.2 Create a post method
        #8.2.1 Query the user from the DB with the name provided in the request
        #8.2.2 Set the user's id to sessions under the user_id key
        #8.2.3 Create a response to the client with the user's data

# 9.✅ Create a route that checks to see if the User is currently in sessions
    # 9.1 Use add_resource to add an authorized endpoint
    # 9.2 Create a Get method
        #9.2.1 Check to see if the user_id is in session
        #9.2.2 If found query the user and send it to the client
        #9.2.3 If not found return a 401 Unauthorized error


# 10.✅ Create a Logout route
    #10.1 Use add_resource to add a logout endpoint
    #10.2 Create a delete method
        # 8.2.1 Set the user_id in sessions to None
        # 8.2.1 Create a response with no content and a 204
    #10.3 Test out your route with the client or Postman

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: Sorry the resource you are looking for does not exist",
        404
    )

    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)