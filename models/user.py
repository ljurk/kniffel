from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def _getPrimaryKey(self):
        print("unique columns")
        return [k.name for k in User.__mapper__.primary_key]
    def _getUniqueColumns(self):
        return [c for c in User.__table__.columns if c.unique]

    def _toDict(self):
        tempDict = self.__dict__
        if '_sa_instance_state' in tempDict:
            del tempDict['_sa_instance_state']
        return tempDict
