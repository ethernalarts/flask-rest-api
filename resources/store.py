from db import db
from flask import request
from models import StoreModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import *

blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, store_id, new_store_data):
        store = StoreModel.query.get(store_id)
        if store:
            store.store_name = new_store_data["store_name"]
        else:
            store = StoreModel(**new_store_data, store_id=store_id)
        db.session.add(store)
        db.session.commit()
        return store

    @blp.response(200)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store has been deleted"}


@blp.route("/stores")
class StoresList(MethodView):
    @blp.response(201, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


@blp.route("/store/create")
class CreateStore(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, new_store_data):
        store = StoreModel(**new_store_data)
        try:
            db.session.add(store)
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        else:
            db.session.commit()

        return store
