from marshmallow import Schema, fields

class PlainItemSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.String(required=True)
  price = fields.Float(required=True)
  
class PlainStoreSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.String(required=True)
  
class PlainTagSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.String(required=True)
  
class ItemSchema(PlainItemSchema):
  store_id = fields.Int(required=True,load_only=True)
  store = fields.Nested(PlainStoreSchema(),dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

  
class ItemUpdateSchema(Schema):
  name = fields.String()
  price = fields.Float()
  store_id = fields.Int()


  
class StoreSchema(PlainStoreSchema):
  items  = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)
  
  
class TagSchema(PlainTagSchema):
  store_id = fields.Int(load_only=True)
  store = fields.Nested(PlainStoreSchema(),dump_only=True)
  items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
  
class TagAndItemSchema(Schema):
  mesage = fields.String()
  item = fields.Nested(ItemSchema())
  tags = fields.Nested(TagSchema())
  
class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.String(required=True)
  password = fields.String(required=True,load_only=True)
  