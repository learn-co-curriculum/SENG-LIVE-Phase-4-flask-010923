#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py` 
# done

# 2. ✅ Set Up Imports
# import Flask from flask
# later, also import jsonify and make_response
# import Migrate from flask_migrate
# import db and newly created Production from Models
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Production

# 3. ✅ Initialize the App
app = Flask(__name__)
    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False`

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set the migrations with `migrate = Migrate(app, db)`
migrate = Migrate(app, db)
    # Finally, initialize the application with `db.init_app(app)`
db.init_app(app)

# 4. ✅ Migrate
    # `cd` into the `server` folder
    # Run in Terminal
		# export FLASK_APP=app.py
		# export FLASK_RUN_PORT=5555
		# flask db init
		# flask db revision --autogenerate -m 'Create tables productions'
		# flask db upgrade

# 5. ✅ Navigate to `seed.rb`
# seed data created


# 6. ✅ Routes
@app.route('/')
def index():
    return "<h1>Hello World!</h1>"


# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route
@app.route("/productions/<int:id>/image")
def productions_by_id(id):
    production = db.session.query(Production).filter_by(id=id).first()
    return f"<img src='{production.image}' />"


# 9.✅ Update the route to find a `production` by its `title` and send it to our browser
@app.route("/productions/title/<string:title>")
def productions(title):
    production = db.session.query(Production).filter(Production.title.like(f"%{title}%")).first()
    if production is None:
        fail_response = make_response(
            f"<h1>I could not find title by {title}</h1>",
            500
            )
        return fail_response
    else:
        production_response = {
            "id": production.id,
            "title": production.title,
            "genre": production.genre,
            "budget": production.budget,
            "image": production.image,
            "director": production.director,
            "description": production.description,
            "ongoing": production.ongoing,
            "created_at": production.created_at,
            "updated_at": production.updated_at
        }


        response = make_response(
            jsonify(production_response),
            200
        )

        # response = make_response(
        #     jsonify(production_response),
        #     200
        # )

        return response


    
    

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5555, debug=True)
