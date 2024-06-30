#add experiment:Vtext, LLMAnswerImg,QCode,Score
from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base

#submit type:
#change score:Uid,Score,Explanation,Qid
#add experiment:Vtext, LLMAnswerImg,QCode,Score
#add course: CourseName, Explanation
#add helptopic: Score,LLM_Prompt,PromptAnswerImg,Hid

class AddExperiment(Base):
    Rid = Column(Integer, primary_key=True, autoincrement=True)
    VText = Column(String(1000))
    LLMAnswerImg = Column(String(100))
    QCode = Column(String(100))
    Score = Column(Integer)

    def __init__(self,vtext,llmanswerImg,qcode,score):
        super(AddExperiment, self).__init__()
        self.VText = vtext
        self.LLMAnswerImg = llmanswerImg
        self.QCode = qcode
        self.Score = score
        

