#add course: CourseName, Explanation，category

from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base

class AddCourse(Base):
    Rid = Column(Integer, primary_key=True, autoincrement=True)
    Explanation = Column(String(500))
    CourseName = Column(String(100))
    Category = Column(String(1000))

    def __init__(self,explanation,coursename, category):
        super(AddCourse, self).__init__()
        
        self.Explanation = explanation
        self.CourseName = coursename
        self.Category = category

