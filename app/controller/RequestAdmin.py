from platform import node
from flask import Blueprint, render_template, redirect, request, session, url_for
from app.models.addCourse import AddCourse
from app.models.course import Course
from app.models.llm_answer import LLM_Answer
from app.models.addExperiment import AddExperiment
from app.models.change_score import ChangeScore
from app.models.base import db
from app.models.topicQA import TopicQA
from app.models.addHelptopic import AddHelptopic

RequestBP = Blueprint('RequestAdmin', __name__)


# Maintain user information
@RequestBP.context_processor
def my_context_processor():
    Uid = session.get('Uid')
    UserType = session.get('UserType')
    print(Uid)
    if Uid:
        return {'Uid': Uid, 'UserType': UserType}
    else:
        return redirect(url_for('user.login'))


# admin index page
@RequestBP.route('/request', methods=['POST', 'GET'])
def Request():
    Uid = session.get('Uid')
    if Uid:
        return render_template('Request.html')
    else:
        return redirect(url_for('user.login'))

    # admin look all experiment request


@RequestBP.route('/request/add_experiment')
def R_Add_Experiment():
    Uid = session.get('Uid')
    if Uid:
        experiments = AddExperiment.query.all()
        import base64
        for exp in experiments:
            img_stream = ''
            with open(exp.LLMAnswerImg, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
            exp.LLMAnswerImg = img_stream
        return render_template('R_Add_Experiment.html', experiments=experiments)
    else:
        return redirect(url_for('user.login'))


# admin delete experiment request (reject the request)
@RequestBP.route('/request/delete_experiment/<int:AnswerID>', methods=['POST'])
def delete_experiment(AnswerID):
    Uid = session.get('Uid')
    if Uid:
        experiment = AddExperiment.query.get(AnswerID)
        if experiment:
            db.session.delete(experiment)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


# admin pass the experiment request (agree the request)
@RequestBP.route('/request/move_experiment/<int:Rid>', methods=['POST'])
def move_experiment(AnswerID):
    Uid = session.get('Uid')
    if Uid:
        experiment = LLM_Answer.query.get(AnswerID)
        if experiment:
            new_experiment = LLM_Answer(AnswerID=AnswerID, vtext=experiment.vText, llm_solution=experiment.llmanswerImg,
                                        LLM_Score=experiment.score, Qid=experiment.Qid)
            db.session.add(new_experiment)
            db.session.delete(experiment)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


# admin look all change score request
@RequestBP.route('/request/change_score')
def R_Change_Score():
    Uid = session.get('Uid')
    if Uid:
        scores = ChangeScore.query.all()
        return render_template('R_Change_Score.html', scores=scores)
    else:
        return redirect(url_for('user.login'))


# admin reject the request
@RequestBP.route('/request/delete_chaning/<int:Rid>', methods=['POST'])
def delete_chaning(Rid):
    Uid = session.get('Uid')
    if Uid:
        score = ChangeScore.query.get(Rid)
        if score:
            db.session.delete(score)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


# admin agree the request
@RequestBP.route('/request/move_chaning/<int:Rid>', methods=['POST'])
def move_chaning(Rid):
    Uid = session.get('Uid')
    if Uid:
        score = ChangeScore.query.get(Rid)
        if score:
            new_score = LLM_Answer(AnswerID=generate_unique_cnumber(), vtext=generate_unique_cnumber(),
                                   llm_solution=generate_unique_cnumber(), LLM_Score=score.Score, Qid=score.Qid)
            db.session.add(new_score)
            db.session.delete(score)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


# admin look all add course request
@RequestBP.route('/request/add_course')
def R_Add_Course():
    Uid = session.get('Uid')
    if Uid:
        courses = AddCourse.query.all()
        return render_template('R_Add_Course.html', courses=courses)
    else:
        return redirect(url_for('user.login'))


# admin reject the request
@RequestBP.route('/request/delete_course/<int:Rid>', methods=['POST'])
def delete_course(Rid):
    Uid = session.get('Uid')
    if Uid:
        course = AddCourse.query.get(Rid)
        if course:
            db.session.delete(course)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


# admin agree the request
@RequestBP.route('/request/move_course/<int:Rid>', methods=['POST'])
def move_course(Rid):
    Uid = session.get('Uid')
    if Uid:
        course = AddCourse.query.get(Rid)
        if course:
            new_course = Course(CNumber=generate_unique_cnumber(), cname=course.CourseName, cat=course.Category)
            db.session.add(new_course)
            db.session.delete(course)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


def generate_unique_cnumber():
    pass


# admin look all add helptopic request
@RequestBP.route('/request/add_help_topic')
def R_Add_Help_Topic():
    Uid = session.get('Uid')
    if Uid:
        htopics = AddHelptopic.query.all()
        import base64
        for h in htopics:
            img_stream = ''
            with open(h.PromptAnswerImg, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
            h.PromptAnswerImg = img_stream
        return render_template('R_Add_Help_Topic.html', htopics=htopics)
    else:
        return redirect(url_for('user.login'))


# admin reject the request
@RequestBP.route('/request/delete_course/<int:Rid>', methods=['POST'])
def delete_htopic(Rid):
    Uid = session.get('Uid')
    if Uid:
        htopic = AddHelptopic.query.get(Rid)
        if htopic:
            db.session.delete(htopic)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))


# admin agree the request
@RequestBP.route('/request/move_htopic/<int:Rid>', methods=['POST'])
def move_htopic(Rid):
    Uid = session.get('Uid')
    if Uid:
        htopic = AddHelptopic.query.get(Rid)
        if htopic:
            new_htopic = TopicQA(Tid=htopic.Tid, llm_name=generate_unique_cnumber(), llm_prompt=htopic.llm_prompt,
                                 promptanswerImg=htopic.promptanswerImg)
            db.session.add(new_htopic)
            db.session.delete(htopic)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return "Course not found"
    else:
        return redirect(url_for('user.login'))
