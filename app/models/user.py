from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class User(Base):
    Uid = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(100), unique=True, nullable=True)
    _Password = Column('password', String(100))
    UserType = Column(String(20))

    def __init__(self, email, pwd, utype):
        super(User, self).__init__()
        self.Email = email
        self._Password = pwd
        self.UserType = utype