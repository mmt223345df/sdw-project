#add helptopic: Score,LLM_Prompt,PromptAnswerImg,Hid
from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base

class AddHelptopic(Base):
    Rid = Column(Integer, primary_key=True, autoincrement=True)
    Score = Column(Integer)
    Tid = Column(String(1000))#HelpTopic id
    LLM_Prompt = Column(String(1000))
    PromptAnswerImg = Column(String(1000))

    def __init__(self,tid,llm_prompt,promptanswerImg,score):
        super(AddHelptopic, self).__init__()
        self.Tid = tid
        self.LLM_Prompt = llm_prompt
        self.PromptAnswerImg = promptanswerImg
        self.Score = score
        
        

