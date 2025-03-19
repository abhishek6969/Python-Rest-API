
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort , Blueprint
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import get_jwt, jwt_required


blp  = Blueprint('items' , __name__ , description ="item operations")


@blp.route('/item/<int:item_id>')
class item(MethodView):
  @jwt_required(fresh=False)
  @blp.response(200 , ItemSchema)
  def get(self , item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item
  @jwt_required(fresh=True)
  def delete(self , item_id):
    jwt = get_jwt()
    if not jwt.get('is_admin'):
      return {"message": "Admin privilege required."} , 401
    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return {'message':'Item deleted successfully'}
  
  @blp.arguments(ItemUpdateSchema)
  @blp.response(200 , ItemSchema)
  def put(self , item_data , item_id):
    item = ItemModel.query.get(item_id)
    if item :
      item.price = item_data['price']
      item.name = item_data['name']
      item.store_id = item_data['store_id']
    else:
      item = ItemModel(id=item_id,**item_data)
    db.session.add(item)
    db.session.commit()
    return item
    
  
@blp.route('/item')
class itemlist(MethodView):
  @blp.arguments(ItemSchema)
  @blp.response(201 , ItemSchema)
  def post(self, item_data):
    item = ItemModel(**item_data)
    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError:
      abort(500 , message='Error Occured.')
    except IntegrityError:
      abort(400 , message='Item already exists.')
    return item , 201

  @blp.response(200 , ItemSchema(many=True))
  def get(self):
    return ItemModel.query.all()