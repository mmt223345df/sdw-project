from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base


class Save(Base):
    Sid = Column(Integer, primary_key=True, autoincrement=True)
    Uid = Column(Integer)
    QCode = Column(String(100))
    Q_Text = Column(String(1000))
    LLM_Name = Column(String(20))
    LLMAnswerImg = Column(String(100))
    LLM_Score = Column(Integer)

    def __init__(self, uid,qcode,q_text,llm_name,llmanswerImg, llm_score):
        super(Save, self).__init__()
        self.Uid = uid
        self.QCode = qcode
        self.Q_Text = q_text
        self.LLM_Name = llm_name
        self.LLMAnswerImg = llmanswerImg
        self.LLM_Score = llm_score
