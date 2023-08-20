from flask import request,jsonify
from app import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from .models import User,ClassRoom
from apps.utils import serialize_users


class UserAuthView(Resource):

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)
        return {"msg": f"Hello {current_user.username} !"}

    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        u = User.query.filter_by(username=username).one_or_none()
        if not u or not u.check_password(password):
            return {"msg":"Wrong username or password"}, 401

        access_token = create_access_token(identity=u.id)
        return {"access_token":access_token}


class RegisterUser(Resource):
    @jwt_required()
    def post(self):
        """
        Create User by manager
        """
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if not current_user.is_manager():
            return {"msg": "access Dinaide"}

        username = request.json.get("username", None)
        password = request.json.get("password", None)
        role = request.json.get("role", None)

        errors = []

        if username is None:
            errors.append("Need send Username")
        elif User.query.filter_by(username=username).first():
            errors.append("Username Must be unique")

        if password is None:
            errors.append("Need send Password")
        elif len(password) <= 4:
            errors.append("Password Is Short")

        if role not in ['student','teacher','consultant']:
            errors.append("Must Select 'student' or 'teacher' or 'consultant' for role")

        if len(errors) > 0:
            return {"msg":"fix problems","problems":errors}

        try:
            u = User()
            u.username = username
            u.set_password(password)
            u.role = role
            db.session.add(u)
            db.session.commit()
            return {"msg":f"{role} created with id {u.id}"}, 201
        except IntegrityError:
            return {"msg", "Bad Request"}


class ClassRoomCreate(Resource):
    @jwt_required()
    def post(self):
        """
        Create ClassRoom by manager
        """
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if not current_user.is_manager():
            return {"msg": "access Dinaide"}

        name = request.json.get("name", None)
        if name is None:
            return {"msg":"must send 'name' classsroom"}, 401

        try:
            cr = ClassRoom(name=name)
            db.session.add(cr)
            db.session.commit()
            return {"msg":f"Created ClassRoom {name} with id {cr.id}"}
        except IntegrityError:
            return {"msg":"Bad Request"},401


class AddStudentOrTeacherToClassRoom(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if not current_user.is_manager():
            return {"msg": "access Dinaide"}

        class_room_id = request.json.get("classroom", None)
        user_id = request.json.get("user", None)

        if class_room_id is None or user_id is None:
            return {"msg":"Must Send user and classroom"},401

        try:
            user = User.query.get(ident=user_id)
            user.classroom_id = class_room_id
            db.session.add(user)
            db.session.commit()

            return {"msg": f"User {user_id} Joined to Class {class_room_id}"}
        except IntegrityError:
            return {"msg":"Bad Request"}, 401


class ListUsersView(Resource):
    """
    return list all of users with detail
    """
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if not current_user.is_manager():
            return {"msg": "access Dinaide"}

        users = serialize_users(User.query.all())

        return {"users": users}