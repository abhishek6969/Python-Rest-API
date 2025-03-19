from flask.views import MethodView
from flask_smorest import abort , Blueprint
from blocklist import blocklist
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256 as sha256
from schemas import UserSchema
from flask_jwt_extended import create_access_token, get_jwt, jwt_required , create_refresh_token , get_jwt_identity

blp  = Blueprint('users' , __name__ , description ="User operations")

@blp.route('/register')
class Register(MethodView):
  @blp.arguments(UserSchema)
  def post(self, user_data):
    if UserModel.query.filter(UserModel.username == user_data['username']).first():
      abort(409 , message='User already exists.')
    user = UserModel(
      username = user_data['username'],
      password = sha256.hash(user_data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created successfully."} , 201

@blp.route('/user/<int:user_id>')
class User(MethodView):
  def get(self , user_id):
    user = UserModel.query.get_or_404(user_id)
    return {"username": user.username}
  
  def delete(self , user_id):
    user = UserModel.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted."}
  
@blp.route('/login')
class userLogin(MethodView):
  @blp.arguments(UserSchema)
  def post(self , user_data):
    user = UserModel.query.filter(UserModel.username == user_data['username']).first()
    if  user and  sha256.verify(user_data['password'] , user.password):
      access_token = create_access_token(identity=str(user.id),fresh=True)
      refresh_token = create_refresh_token(identity=str(user.id))
      return {"access_token": access_token , "refresh_token": refresh_token} , 200
    else:
      return {"message": "Invalid credentials."} , 401
    
@blp.route('/logout')
class userLogout(MethodView):
  @jwt_required()
  def post(self):
    jwt = get_jwt()
    blocklist.add(jwt['jti'])
    return {"message": "Successfully logged out."} , 200

@blp.route('/refresh')
class userRefresh(MethodView):
  @jwt_required(refresh=True)
  def post(self):
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user , fresh=False)
    return {"access_token": new_token} , 200
