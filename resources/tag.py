from flask.views import MethodView
from flask_smorest import abort , Blueprint
from schemas import TagSchema , TagAndItemSchema
from models import StoreModel , TagModel , ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp  = Blueprint('tags' , __name__ , description ="tag operations")

@blp.route('/store/<int:store_id>/tag')
class TagInStore(MethodView):
  @blp.response(200,TagSchema(many=True))
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store.tags.all()
  @blp.arguments(TagSchema)
  @blp.response(201 , TagSchema)
  def post(self, tag_data, store_id):
    # if TagModel.query.filter(TagModel.name == tag_data['name'] and TagModel.id == tag_data['name']).first():
    #   abort(400 , message='Tag already exists in store.')
    tag = TagModel(**tag_data , store_id=store_id)
    try:
      db.session.add(tag)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500 , message=str(e))
    except IntegrityError:
      abort(400 , message='Tag already exists.')
    return tag
      

@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
  @blp.response(200,TagSchema)
  def get(self , tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return tag
  @blp.response(
    202,
    description="Deletes a tag if no item is tagged with it.",
    example={"message": "Tag deleted."},
  )
  @blp.alt_response(404, description="Tag not found.")
  @blp.alt_response(
    400,
    description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
  )
  def delete(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)

    if not tag.items:
      db.session.delete(tag)
      db.session.commit()
      return {"message": "Tag deleted."}
    abort(
      400,
      message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
    )

@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagToItem(MethodView):
  @blp.response(201,TagSchema)
  def post(self , item_id , tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)
    item.tags.append(tag)
    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500 , message=str(e))
    return tag
  @blp.response(200,TagAndItemSchema)
  def delete(self , item_id , tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)
    item.tags.remove(tag)
    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500 , message=str(e))
    return {'message':'Tag removed from item' , 'item':item , 'tag':tag}