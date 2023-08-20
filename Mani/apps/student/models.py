from app import db
from datetime import datetime
from sqlalchemy import Column,Integer,Table,ForeignKey,String,DateTime

__all__ = [
    'Grade'
]

class Grade(db.Model):
    __tablename__ = 'grade'
    id = Column(Integer,primary_key=True)

    student_id = Column(Integer,ForeignKey('user.id'),unique=True)
    student = db.relationship('User',back_populates='grade')
    grade = Column(Integer)
    description = Column(String(64))

    created = Column(DateTime(),default=datetime.now)
