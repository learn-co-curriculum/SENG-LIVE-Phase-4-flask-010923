#!/usr/bin/env python3
# 📚 Review With Students:
    # REST
    # Status codes
    # Error handling 
# Set up:
    # cd into server and run the following in the terminal
    # export FLASK_APP=app.py
    # export FLASK_RUN_PORT=5000
    # flask db init
    # flask db revision --autogenerate -m'Create tables' 
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


from flask import Flask, request, make_response, abort
from flask_migrate import Migrate

from flask_restful import Api, Resource

# 2.✅ Import NotFound from werkzeug.exceptions for error handling
from werkzeug.exceptions import NotFound

from models import db, Production, CastMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

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
# 4.✅ If a production is not found raise the NotFound exception
        if not production:
            abort(404, 'The Production you were looking for was not found!')
        
        production_dict = production.to_dict()
        response = make_response(
            production_dict,
            200
        )
        
        return response

# 5.✅ Patch

    def patch(self,id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            abort(404, 'The Production you were trying to update was not found!')
        
        request_json = request.get_json()
        for key in request_json:
            setattr(production,key,request_json[key])
        
        db.session.add(production)
        db.session.commit()

        response = make_response(
            production.to_dict(),
            200
        )

        return response


 
        
# 6.✅ Delete
    def delete(self, id):
            production = Production.query.filter_by(id=id).first()
            if not production:
                abort(404, 'The Production you were trying to delete was not found!')

            db.session.delete(production)
            db.session.commit()

            response = make_response('', 204)

            return response

 

api.add_resource(ProductionByID, '/productions/<int:id>')



#Student Exercises 
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

#'/cast_members/<int:id>'
class CastMembersByID(Resource):
    def get(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, 'The cast member you are looking for was not found')
        response = make_response(
            cast_member.to_dict(),
            200
        )

        return response
    #patch
    def patch(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, 'The cast member you were trying to update was not found!')

        request_json = request.get_json()
        for key in request_json:
            setattr(cast_member, key, request_json[key])

        db.session.add(cast_member)
        db.session.commit()

        response = make_response(
            cast_member.to_dict(),
            200
        )

        return response

    def delete(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, 'The cast member you were trying to delete can not be found!')
        
        db.session.delete(cast_member)
        db.session.commit()

        response = make_response('',204)

        return response

api.add_resource(CastMembersByID, '/cast_members/<int:id>')


# 3.✅ use the @app.errorhandler() decorator to handle Not Found
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "NotFound: Sorry the resource you are looking for can not be found!",
        404
    )
    return response


# To run the file as a script
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
