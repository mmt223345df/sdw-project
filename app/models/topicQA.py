#topicQA.py
#tid, llm_name,llm_prompt,PromptAnswerImg,score

from sqlalchemy import Column, ForeignKey, String, Integer
from app.models.base import Base

class TopicQA(Base):
    Hid = Column(Integer, primary_key=True, autoincrement=True)
    Tid = Column(Integer, ForeignKey('topic.Tid'))
    LLM_Name = Column(String(100))
    LLM_Prompt = Column(String(1000))
    PromptAnswerImg = Column(String(1000))
    Help_score = Column(Integer)

    def __init__(self,llm_name,tid,llm_prompt,promptanswerImg,help_score):
        super(TopicQA, self).__init__()
        self.LLM_Name = llm_name
        self.Tid = tid
        self.LLM_Prompt = llm_prompt
        self.PromptAnswerImg = promptanswerImg
        self.Help_score = help_score
