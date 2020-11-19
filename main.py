import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import request

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False

sqlite_connection_string = f'postgres://wquwwskhrostuu:3060fc022870e6b07fd4cbe169d8e74e221eea4b854de98c095e79b16ba1877c@ec2-3-213-106-122.compute-1.amazonaws.com:5432/d73s790537cjfv'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://wquwwskhrostuu:3060fc022870e6b07fd4cbe169d8e74e221eea4b854de98c095e79b16ba1877c@ec2-3-213-106-122.compute-1.amazonaws.com:5432/d73s790537cjfv'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'user'
    user_name = db.Column(db.String(140), primary_key=True)
    score = db.Column(db.Integer)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("user_name", "score")


db.create_all()

user_schema = UserSchema(many=True)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/update_user_name', methods=['GET'])
def update_user_name():
    first_name = request.args.get('first_name')
    second_name = request.args.get('second_name')
    user = db.session.query(User).filter_by(user_name=first_name).first()
    result = "OK"
    if user:
        user.user_name = second_name
        db.session.commit()
    else:
        result = "User do not exist"
    return result


@app.route('/set_new_user', methods=['GET'])
def set_new_user():
    user_name = request.args.get('user_name')
    user = db.session.query(User).filter_by(user_name=user_name).first()
    result = "OK"
    if user:
        result = "User exist"
    else:
        new_user = User(user_name=user_name, score=0)
        db.session.add(new_user)
        db.session.commit()
    return result


@app.route('/set_score', methods=['GET'])
def set_score():
    user_name = request.args.get('user_name')
    score = request.args.get('score')
    user = db.session.query(User).filter_by(user_name=user_name).first()
    if user:
        user.score = score
    else:
        new_user = User(user_name=user_name, score=score)
        db.session.add(new_user)
    db.session.commit()
    return "OK"


@app.route('/get_my_score', methods=['GET'])
def get_my_score():
    result = ""
    user_name = request.args.get('user_name')
    user = db.session.query(User).filter_by(user_name=user_name).first()
    if user:
        result = str(user.score)
    return result


@app.route('/get_all_score', methods=['GET'])
def get_all_score():
    result = ""
    users = db.session.query(User).filter(User.score != 0).order_by(User.score.desc()).limit(15).all()
    if users:
        print(users)
        result = user_schema.dump(users)
    return jsonify(result)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
