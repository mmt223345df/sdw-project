#save_student.py
#sid, llm_name,llm_prompt,PromptAnswerImg,score,uid

from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base

class Save_stu(Base):
    Sid = Column(Integer, primary_key=True, autoincrement=True)
    Uid = Column(Integer)
    Tid = Column(Integer, ForeignKey('topic.Tid'))
    LLM_Name = Column(String(100))
    LLM_Prompt = Column(String(1000))
    PromptAnswerImg = Column(String(1000))
    Help_score = Column(Integer)

    def __init__(self,uid,tid,llm_name,llm_prompt,promptanswerImg,help_score):
        super(Save_stu, self).__init__()
        self.Uid = uid
        self.Tid = tid
        self.LLM_Name = llm_name
        self.LLM_Prompt = llm_prompt
        self.PromptAnswerImg = promptanswerImg
        self.Help_score = help_score

        
        

