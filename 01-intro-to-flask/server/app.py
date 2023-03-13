#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import db, Production

# 3. ✅ Initialize the App
  
    
    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app,db)
db.init_app(app)
    

 # 4. ✅ Migrate 
  # Run in Terminal
		# export FLASK_APP=app.py
		# export FLASK_RUN_PORT=5555
		# flask db init
		# flask db revision --autogenerate -m 'Create tables productions'
		# flask db upgrade

# 5. ✅ Navigate to `seed.rb`
# 12. ✅ Routes

# 13. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

@app.route('/')
def index():
    return '<h1>Hello World</h1>'
#Student Challenge: Create a route to '/image' that displays an image on the Browser
#/image
@app.route('/image')
def image():
    return '<img src=https://images.unsplash.com/photo-1520315342629-6ea920342047?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80 />'


# 14. ✅ Create a dynamic route
# @app.route('/productions/<string:title>')
#  def production(title):
#     return f'<h1>{title}</h1>'

# 15.✅ Update the route to find a `production` by its `title` and send it to our browser
@app.route('/productions/<string:title>')
def production(title):
    production = Production.query.filter(Production.title == title).first()
    production_response = {
        "title": production.title, 
        "genre": production.genre,
        "director": production.director,
        "description":production.description,
        "image": production.image,
        "budget":production.budget,
        "ongoing":production.ongoing
    }
    response = make_response(
        jsonify(production_response),
        200
    )
    return response



# 16.✅ Demo request context 
# @app.route('/context')
# def context():
#     import ipdb; ipdb.set_trace()
#     return f'<h1>Path{request.path} Host:{request.host}</h1>'

# 17.✅ Request Hooks
# @app.before_request: runs a function before each request.
# @app.before_first_request: runs a function before the first request (but not subsequent requests).
# @app.after_request: runs a function after each request.
# @app.teardown_request: runs a function after each request, even if an error has occurred.
@app.before_request
def runs_before():
    current_user={"user_id":1, "username":"rose"}
    print(current_user)
   

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
