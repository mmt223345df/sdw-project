from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base


class AssignQ(Base):
    __tablename__="assignq"
    Qid = Column(Integer, primary_key=True, autoincrement=True)
    CNumber = Column(Integer, ForeignKey('course.CNumber'))# Used to link courses.
    QCode = Column(String(100))
    QText = Column(String(1000))
    VCode = Column(String(100))
    VText = Column(String(1000))

    def __init__(self,cnumber,qcode,qtext,vcode,vtext):
        super(AssignQ, self).__init__()
        self.CNumber = cnumber
        self.QCode = qcode
        self.QText = qtext
        self.VCode = vcode
        self.VText = vtext