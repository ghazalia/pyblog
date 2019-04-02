from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields as ma_field
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app, version='1.0', title='Blog Apis')

db = SQLAlchemy(app)

# blog namespace
ns_blog = api.namespace('blogs', description='Blog Post operations')
ns_user = api.namespace('users', description='User Account Operations')


class BlogPostModel(db.Model):
    """
    Blogpost Model
    """
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow)


class UserModel(db.Model):
    '''
    User Model
    '''
    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow())
    blogposts = db.relationship(
        'BlogPostModel', backref='users', lazy='dynamic')


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
@ns_user.route('/')
class Users(Resource):
    @ns_user.doc('list_user')
    @ns_user.marshal_list_with(user_model)
    def get(self):
        users = UserModel.query.all()
        userSchema = UserSchema(many=True)
        return userSchema.dump(users)

    @ns_user.doc('create_user')
    @ns_user.expect(user_model)
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

        emailStatus = UserModel.query.filter_by(email=email).first()
        if emailStatus is None:
            # create new author
            new_user = UserModel(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return {'result': 'user created'}, 201
        return {'error': 'email already existed'}, 400


if __name__ == '__main__':
    app.run(debug=True)
