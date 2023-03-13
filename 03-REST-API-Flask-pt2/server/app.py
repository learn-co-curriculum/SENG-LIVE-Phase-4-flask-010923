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
from flask import Flask, request, make_response, abort
from flask_migrate import Migrate

from flask_restful import Api, Resource

# 1.✅ Import NotFound from werkzeug.exceptions for error handling


from models import db, Production, CrewMember

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
        new_production = Production(
            title=request.form['title'],
            genre=request.form['genre'],
            budget=int(request.form['budget']),
            image=request.form['image'],
            director=request.form['director'],
            description=request.form['description'],
            ongoing=bool(request.form['ongoing']),
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
# 3.✅ If a production is not found raise the NotFound exception
    
        production_dict = production.to_dict()
        response = make_response(
            production_dict,
            200
        )
        
        return response

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

# 2.✅ use the @app.errorhandler() decorator to handle Not Found
    # 2.1 Create the decorator and pass it NotFound
    # 2.2 Use make_response to create a response with a message and the status 404
    # 2.3 return t he response


# To run the file as a script
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)