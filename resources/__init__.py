from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

print(__all__)
from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse
from sqlalchemy import exc
from flask import abort
from models import db

class BaseResource(Resource):
    def __init__(self):
        # initialize parser
        self.parser = reqparse.RequestParser()
        self.keys = []
        if not hasattr(self, 'model'):
            return
        for key in self.model.__dict__.keys():
            # ignore builtin vars and methods
            if key.startswith('_'):
                continue
            self.keys.append(key)
            self.parser.add_argument(key)

    def post(self):
        args = self.parser.parse_args()
        print(args)
        del args['id']
        for key, val in args.items():
            if not val:
                return {"error": f"{key} missing"}

        try:
            temp = self.model(**args)
            db.session.add(temp)
            db.session.commit()
            db.session.refresh(temp)
        except exc.IntegrityError as err:
            return {'error': str(err)}
        return temp._toDict()

    def get(self):
        try:
            args = self.parser.parse_args()
            for key in self.keys:
                if args[key]:
                    return self.model.query.filter_by(**{key: args[key]}).first_or_404()._toDict()
            abort(404)
        except BadRequest:
            return {'data': [row._toDict() for row in self.model.query.all()]}

    def delete(self):
        temp = self.model()
        args = self.parser.parse_args()


        pk = temp._getUniqueColumns()
        for key, val in args.items():
            if key in temp._getUniqueColumns() and val:
                print(key)

        if len(pk) > 1:
            return "multi pk"
        pk = pk[0]
        if not args[pk]:
            return {"error": f"{pk} missing"}
        user = self.model.query.filter_by(**{pk: args[pk]}).first_or_404()
        return user._toDict()
