from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base
#topic.py
#Tid, Topic,SubTopic，Courseid

#add helptopic: Score,LLM_Prompt,PromptAnswerImg,Hid
#If SubTopic_name has a value, it is displayed. Otherwise, Topic_name is displayed
class Topic(Base):
    __tablename__="topic"
    Tid = Column(Integer, primary_key=True, autoincrement=True)
    CNumber = Column(Integer, ForeignKey('course.CNumber'))
    Topic_name = Column(String(1000))
    SubTopic_name = Column(String(1000))
    

    def __init__(self,tid,topic_name,subtopic_name,cnumber):
        super(Topic, self).__init__()
        self.Tid = tid
        self.Topic_name = topic_name
        self.SubTopic_name = subtopic_name
        self.CNumber = cnumber