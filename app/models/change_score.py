#change score:Uid,Score,Explanation,Qid

from sqlalchemy import Column, ForeignKey, String, Integer, orm
from app.models.base import Base
from app.models.base import db

#submit type:
#change score:Uid,Score,Explanation,Qid
#add experiment:Vtext, LLMAnswerImg,QCode,Score
#add course: CourseName, Explanation
#add helptopic: Score,LLM_Prompt,PromptAnswerImg,Hid

class ChangeScore(Base):
    Rid = Column(Integer, primary_key=True, autoincrement=True)
    Uid = Column(Integer)
    Qid = Column(Integer, ForeignKey('assignq.Qid'))
    Explanation = Column(String(500))
    Score = Column(Integer)

    def __init__(self,uid,qid,explanation,score):
        super(ChangeScore, self).__init__()
        self.Uid = uid
        self.Qid = qid
        self.Explanation = explanation 
        self.Score = score
def save_to_database(uid, qid, explanation, score):
    saving = ChangeScore(
        Uid=uid,
        Qid=qid,
        Explanation=explanation,
        Score=score
    )
    db.session.add(saving)
    db.session.commit()
        

