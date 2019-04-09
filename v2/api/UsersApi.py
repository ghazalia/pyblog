from flask_restplus import Namespace, Resource, fields
from commons import bcrypt, db
from model.Users import UserModel
from marshmallow import Schema, ValidationError, fields as ma_field

api = Namespace('users', description='User account operations')
# ns_user = api.namespace('users', description='User Account Operations')

# model for swagger
user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='user unique identifier'),
    'name': fields.String(required=True, description='user name'),
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='password')
})

blog_model = api.model('Blog', {
    'id': fields.Integer(readOnly=True, description='user unique identifier'),
    'title': fields.String,
    'contents': fields.String,
    'owner_id': fields.Integer
})


class UserSchema(Schema):
    id = ma_field.Int(dump_only=True)
    name = ma_field.Str()
    email = ma_field.Str()
    password = ma_field.Str()

# route definition
@api.route('/')
class UsersList(Resource):
    @api.doc('list_user')
    @api.marshal_list_with(user_model)
    def get(self):
        users = UserModel.query.all()
        userSchema = UserSchema(many=True)
        return userSchema.dump(users)

    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        '''Create a new user'''
        try:
            user_model = api.payload
        except ValidationError as err:
            return {'error': err.messages}, 422

        # initialize fields
        name = user_model['name']
        email = user_model['email']
        password = user_model['password']
        password_hashed = bcrypt.generate_password_hash(
            password, 10)
        emailStatus = UserModel.query.filter_by(email=email).first()
        if emailStatus is None:
            # create new user
            new_user = UserModel(name=name, email=email,
                                 password=password_hashed)
            db.session.add(new_user)
            db.session.commit()

            return {'result': 'user created'}, 201
        return {'error': 'email already existed'}, 400
