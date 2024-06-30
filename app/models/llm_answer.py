from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base


class LLM_Answer(Base):
    AnswerID = Column(Integer, primary_key=True, autoincrement=True)
    LLM_Name = Column(String(20))
    LLMAnswerImg = Column(String(100))
    LLM_Score = Column(Integer)
    Comments = Column(String(1000))
    Qid = Column(Integer, ForeignKey('assignq.Qid'))
    
    def __init__(self, llm_name,llmanswerImg, llm_score,com,qid):
        super(LLM_Answer, self).__init__()
        self.LLM_Name = llm_name
        self.LLMAnswerImg = llmanswerImg
        self.LLM_Score = llm_score
        self.Comments = com
        self.Qid = qid