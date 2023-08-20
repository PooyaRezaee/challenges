from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from apps.user.models import User
from app import db
from .models import Grade
from apps.utils import serialize_users

class StudentView(Resource):

    @jwt_required()
    def get(self,pk):
        """
        Read Grade Student
        """
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if not (current_user.is_manager() or current_user.is_consultant() or current_user.is_teachers_student(pk) or current_user.is_self()):
            return {"msg":"You Don't have access"}, 403

        student = User.query.get(ident=pk)
        if student.role != "student":
            return {"msg":"Student Not Found"},404

        grade = student.grade
        if grade:
            return {
                "Grade": grade.grade,
                "Description": grade.description
                }
        else:
            return {"Grade": "Uknow"}


    @jwt_required()
    def post(self,pk):
        """
        Create Grade Student With Teacher
        """
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)



        if not (current_user.is_teacher() or current_user_id.is_manager()):
            return {"msg":"You Don't Have Access"},403
        if not current_user.is_teachers_student(pk):
            return {"msg":"That's not your student"}

        grade = request.json.get("grade")
        description = request.json.get("describtion", None)


        try:
            g = Grade()
            g.grade = grade
            g.description = description
            g.student_id = pk

            db.session.add(g)
            db.session.commit()

            return {"msg":f"grade {grade} registred for student {pk}"}, 201
        except IntegrityError:
            return {"msg":"Student have grade before"}, 401



    @jwt_required()
    def put(self,pk):
        """
        Update Grade Student
        """
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if not (current_user.is_teacher() or current_user_id.is_manager()):
            return {"msg": "You Don't Have Access"}, 403
        if not current_user.is_teachers_student(pk):
            return {"msg": "That's not your student"}

        grade = request.json.get("grade")
        description = request.json.get("description", None)

        student = User.query.get(ident=pk)
        g = student.grade
        if g:
            g.grade = grade
            g.description = description
            db.session.add(g)
            db.session.commit()

            return {"Grade": f"Updated Grade {student.username}"}
        else:
            return {"msg": "User Don't Have Grade"}, 401


    @jwt_required()
    def delete(self,pk):
        """
        expelled Student
        """
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if current_user.is_manager():
            try:
                student = User.query.get(ident=pk)
                if not student.role == 'student':
                    return {"msg": "just can expelled student"}, 401
                student.is_active_at_school = False
                db.session.add(student)
                db.session.commit()
            except IntegrityError:
                return {"msg": "Bad Request"}, 401

            return {"msg": "The student was expelled from school"}
        else:
            return {"msg": "You Don't Have Access"}, 403

class ListUsersView(Resource):
    """Show List ALl Users that Have Access"""
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(ident=current_user_id)

        if current_user.role == 'student':
            return {"msg": "You Don't have access"}, 403

        if current_user.is_teacher():
            users_obj = User.query.filter_by(classroom_id=current_user.classroom_id,role='student')
        elif current_user.is_consultant() or current_user.is_manager():
            users_obj = User.query.filter_by(role='student')
        else:
            print("Uknow Roles !")
            return {"msg":"Internal Problem"},500

        users = serialize_users(users_obj)
        return {"users":users}
