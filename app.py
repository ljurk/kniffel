from flask import Flask, abort
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

from resources import user
#import resources

#from resources.user import UserResource
from models.user import User
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
api = Api(app)
api.add_resource(user.UserResource, '/user')

if __name__ == "__main__":
    db.app = app
    db.init_app(app)
    db.create_all()
    # create example user
    try:
        user = User(username="ljurk", email="lukas.jurk@tu-dresden.de")
        db.session.add(user)
        db.session.commit()
        print(user)
    except Exception as error:
        print(error)
        pass
    app.run(debug=True)
