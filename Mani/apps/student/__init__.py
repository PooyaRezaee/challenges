from flask import Blueprint
from flask_restful import Api


student = Blueprint("student",__name__,url_prefix='/student/')
api = Api(student)

# ---- Views -----
from .views import StudentView,ListUsersView
api.add_resource(StudentView, '<int:pk>/')
api.add_resource(ListUsersView, 'all/')

# ---- Models -----
from .models import *