from flask_restplus import Api
from .UsersApi import api as user_api

api = Api(
    title="Blogs API",
    version="1.0",
    description="A simple Blog API demo"
)

api.add_namespace(user_api)
