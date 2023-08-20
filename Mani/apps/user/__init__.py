from flask import Blueprint
from app import api as api_main
from flask_restful import Api


user = Blueprint("user",__name__,url_prefix='/user/')
api = Api(user)
# ---- Views -----
from .views import UserAuthView,RegisterUser,ClassRoomCreate,AddStudentOrTeacherToClassRoom,ListUsersView

api.add_resource(UserAuthView, '')
api.add_resource(RegisterUser, 'register/')
api.add_resource(ListUsersView, 'all/')
api.add_resource(AddStudentOrTeacherToClassRoom, 'room/') # /user/room/
api_main.add_resource(ClassRoomCreate, '/room/') # /room/

# ---- Models -----
from .models import *