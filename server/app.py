from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at).all()
        messages_ser = [message.to_dict() for message in messages]
        response = make_response(messages_ser, 200)
        return response
    if request.method == "POST":
        data = request.get_json()
        new_message = Message(body=data["body"], username=data["username"])
        db.session.add(new_message)
        db.session.commit()

        response = make_response(new_message.to_dict(), 201)
        return response


@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == "PATCH":
        data = request.get_json()
        setattr(message, "body", data["body"])
        db.session.commit()
        return make_response(message.to_dict(), 200)
    if request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({"message": "message deleted successfully"}), 200)
    return make_response(message.to_dict(), 200)


if __name__ == "__main__":
    app.run(port=4000, debug=True)
