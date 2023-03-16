#!/usr/bin/env python3
# 📚 Review With Students:
    # CORS 
# Set up:
    # cd into server and run the following in Terminal
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5000
        # flask db init
        # flask db revision --autogenerate -m'Create tables' 
        # flask db upgrade 
        # python seed.py
# Running React Together 
    # Verify that gunicorn and honcho have been added to the pipenv
    # Create Procfile.dev in root
        # in Procfile.dev add:
            # web: PORT=3000 npm start --prefix client
            # api: gunicorn -b 127.0.0.1:5000 --chdir ./server app:app
        # In Terminal, run:
            # `honcho start -f Procfile.dev`

from flask import Flask, request, make_response, abort
from flask_migrate import Migrate

from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

# 4.✅ Import CORS from flask_cors, invoke it and pass it app


# 5.✅ Start up the server / client and navigate to client/src/App.js

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
            abort(404, 'The Production you were looking for was not found')
        production_dict = production.to_dict()
        response = make_response(
            production_dict,
            200
        )
        
        return response


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


    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            abort(404, 'The Production you were looking for was not found!')
        db.session.delete(production)
        db.session.commit()

        response = make_response('', 204)
        
        return response
api.add_resource(ProductionByID, '/productions/<int:id>')


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: Sorry the resource you are looking for does not exist",
        404
    )

    return response

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
    def get(self,id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            abort(404, 'The Production you were looking for was not found!')
        
        production_dict = production.to_dict()
        response = make_response(
            production_dict,
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
            production = Production.query.filter_by(id=id).first()
            if not production:
                abort(404, 'The Production you were trying to delete was not found!')

            db.session.delete(production)
            db.session.commit()

            response = make_response('', 204)

            return response
api.add_resource(CastMembersByID, '/cast_members/<int:id>')


# To run the file as a script
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

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