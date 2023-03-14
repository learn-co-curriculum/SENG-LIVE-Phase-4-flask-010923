#!/usr/bin/env python3

# 📚 Review With Students:
    # API Fundamentals
    # MVC Architecture and Patterns / Best Practices
    # RESTful Routing
    # Serialization
    # Postman

# Set Up:
    # In Terminal, `cd` into `server` and run the following:
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5000
        # flask db init
        # flask db revision --autogenerate -m 'Create tables' 
        # flask db upgrade 
        # python seed.py

# Restful

# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|



from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

# 1. ✅ Import `Api` and `Resource` from `flask_restful`
    # ❓ What do these two classes do at a higher level?
from flask_restful import Api, Resource 

from models import db, Production, CastMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Note: `app.json.compact = False` configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# 2. ✅ Initialize the Api
api = Api(app)

# 3. ✅ Create a Production class that inherits from Resource

# 4. ✅ Create a GET (All) Route
class Productions(Resource):
    def get(self):
        # production_list = [{
        #     "title": production.title,
        #     "genre": production.genre,
        #     "director": production.director,
        #     "description": production.description,
        #     "image": production.image,
        #     "budget": production.budget,
        #     "ongoing": production.ongoing,
        # } for production in Production.query.all()]

        production_list = [production.to_dict() for production in Production.query.all()]

        response = make_response(
            production_list,
            200
        )
        return response
    
    def post(self):
        request_json = request.get_json()
       
        new_production = Production(
            title=request_json['title'],
            genre=request_json['genre'],
            budget=request_json['budget'],
            image=request_json['image'],
            director=request_json['director'],
            description=request_json['description'],
            ongoing=request_json['ongoing']
        )
        db.session.add(new_production)
        db.session.commit()

        #new_production.to_dict()
        response = make_response(
            new_production.to_dict(),
            201
        )
        return response
        
api.add_resource(Productions, '/productions')
  
# 5. ✅ Serialization
  

# 10. ✅ Use our serializer to format our response to be cleaner



    
# 11. ✅ Create a POST Route


   
# 12. ✅ Add the new route to our api with `api.add_resource`
#api.add_resource(Productions, '/productions')
    

# 13. ✅ Create a GET (One) route
class ProductionByID(Resource):
    def get(self, id):
        production = Production.query.filter(Production.id == id).first().to_dict()
        response = make_response(
            production,
            200
        )

        return response

api.add_resource(ProductionByID, '/productions/<int:id>')


# 14. ✅ Add the new route to our api with `api.add_resource`
#Students:
#GET All CastMembers '/cast_members'
class CastMembers(Resource):
    def get(self):
        cast_members_list = [cast_member.to_dict() for cast_member in CastMember.query.all()]
    
        response = make_response(
            cast_members_list,
            200
        )
        return response

    def post(self):
        request_json = request.get_json()
        new_cast = CastMember(
            name=request_json['name'],
            role=request_json['role'],
            production_id=request_json['production_id']
        )
        db.session.add(new_cast)
        db.session.commit()

        response_dict = new_cast.to_dict()
        
        response = make_response(
            response_dict,
            201
        )
        return response

api.add_resource(CastMembers, '/cast_members')