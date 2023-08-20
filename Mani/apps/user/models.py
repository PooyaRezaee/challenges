from app import db
from datetime import datetime
from sqlalchemy import Column,Integer,ForeignKey,String,DateTime,Boolean
from werkzeug.security import generate_password_hash,check_password_hash

__all__ = [
    "User",
    "ClassRoom",
]


class ClassRoom(db.Model):
    __tablename__ = 'classroom'

    id = Column(Integer,primary_key=True)

    name = Column(db.String(64),unique=True,nullable=False)
    member = db.relationship('User',back_populates='classroom_member')

    created = Column(DateTime(),default=datetime.now)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True)

    username = Column(db.String(64),unique=True,nullable=False)
    password = Column(String(1280),nullable=False)

    role = Column(db.String(32),nullable=False) # student manager teacher consultant

    # For Teacher,Student
    classroom_id = Column(Integer, ForeignKey('classroom.id'))
    classroom_member = db.relationship('ClassRoom',uselist=False,back_populates='member')
    grade = db.relationship('Grade',uselist=False,back_populates='student')
    is_active_at_school = Column(Boolean, default=False)

    created = Column(DateTime(), default=datetime.now)

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def is_manager(self):
        return self.role == 'manager'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_consultant(self):
        return self.role == 'consultant'

    def is_teachers_student(self,student_id): # This method just for teacher
        if not self.role == 'teacher':
            return False

        student = User.query.get(ident=student_id)
        if student.classroom_id != self.classroom_id:
            return False

        return True

    def is_self(self,id):
        return self.id == id
