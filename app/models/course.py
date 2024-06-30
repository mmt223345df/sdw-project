from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Course(Base):
    __tablename__='course'
    CNumber = Column(Integer, primary_key=True, autoincrement=True)
    CName = Column(String(100))
    Category = Column(String(50))

    def __init__(self, cnumber, cname,cat):
        super(Course, self).__init__()
        self.CNumber = cnumber
        self.CName = cname
        self.Category = cat
