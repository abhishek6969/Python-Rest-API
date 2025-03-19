import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort , Blueprint
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp  = Blueprint('stores' , __name__ , description ="store operations")

@blp.route('/store/<int:store_id>')
class Store(MethodView):
  @blp.response(200 , StoreSchema)
  def get(self , store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store
  
  def delete(self , store_id):
    store = StoreModel.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return {'message':'Store deleted successfully'}
  
  @blp.arguments(StoreSchema)
  @blp.response(200 , StoreSchema)
  def put(self , store_data , store_id):
    store = StoreModel.query.get(store_id)
    if store :
      store.name = store_data['name']
    else:
      store = StoreModel(id=store_id,**store_data)
    db.session.add(store)
    db.session.commit()
    return store

@blp.route('/store')
class StoreList(MethodView):
  @blp.arguments(StoreSchema)
  @blp.response(201 , StoreSchema)
  def post(self,store_data):
    store = StoreModel(**store_data)
    try:
      db.session.add(store)
      db.session.commit()
    except SQLAlchemyError:
      abort(500 , message='Error Occured.')
    except IntegrityError:
      abort(400 , message='Store already exists.')
    return store
  
  @blp.response(200 , StoreSchema(many=True))
  def get(self):
    return StoreModel.query.all()