from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        all_messages = Message.query.order_by(Message.created_at).all()

        json_messages = [message.to_dict() for message in all_messages]

        return make_response(json_messages, 200)
    elif request.method == "POST":
        rq = request.get_json()
        message = Message(
            body = rq.get('body'),
            username = rq.get('username')
        )
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(), 200)
    else:
        return make_response({}, 500)

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if message:
        if request.method == "PATCH":
            rq = request.get_json()
            message.body = rq.get('body')
            
            db.session.add(message)
            db.session.commit()

            return make_response(message.to_dict(), 200)
        elif request.method == "DELETE":
            db.session.delete(message)
            db.session.commit()
            return make_response({}, 200)
        else:
            return f'I got method {request.method}, and ID {id}'
    else:
        return make_response({}, 404)

if __name__ == '__main__':
    app.run(port=4000, debug=True)
