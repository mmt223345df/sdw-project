from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.addCourse import AddCourse
from app.models.addExperiment import AddExperiment
from app.models.change_score import ChangeScore
from app.models.base import db
from app.models.assignq import AssignQ
from app.models.course import Course
from app.models.llm_answer import LLM_Answer
from sqlalchemy import and_, or_

from app.models.save import Save

searchTeacherBP = Blueprint('SearchTeacher', __name__)


# Maintain user information
@searchTeacherBP.context_processor
def my_context_processor():
    Uid = session.get('Uid')
    UserType = session.get('UserType')
    print(Uid)
    if Uid:
        return {'Uid': Uid, 'UserType': UserType}
    else:
        return redirect(url_for('user.login'))
    return {}


# Teacher lookup function
@searchTeacherBP.route('/search_teacher', methods=['POST', 'GET'])
def search_teacher():
    Uid = session.get('Uid')
    if Uid:
        if request.method == 'GET':
            return render_template('searchTeacher.html')
        else:
            sel = request.values.get('searchtea')
            inp = request.form.get("searchteain")
            print(sel, inp)

            if sel == "course_name_number":
                # Match course names or course numbers using fuzzy queries
                results = db.session.query(
                    Course.Category,
                    Course.CName,
                    Course.CNumber,
                    AssignQ.Qid,
                    AssignQ.QText,
                    AssignQ.VText,
                    LLM_Answer.AnswerID,
                    LLM_Answer.LLM_Score
                ).join(AssignQ, Course.CNumber == AssignQ.CNumber
                       ).join(LLM_Answer, AssignQ.Qid == LLM_Answer.Qid
                              ).filter(or_(Course.CName.ilike(f'%{inp}%'), Course.CNumber.ilike(f'%{inp}%'))).all()

            elif sel == "course_category":
                # Match course categories using fuzzy queries
                results = db.session.query(
                    Course.Category,
                    Course.CName,
                    Course.CNumber,
                    AssignQ.Qid,
                    AssignQ.QText,
                    AssignQ.VText,
                    LLM_Answer.AnswerID,
                    LLM_Answer.LLM_Score
                ).join(AssignQ, Course.CNumber == AssignQ.CNumber
                       ).join(LLM_Answer, AssignQ.Qid == LLM_Answer.Qid
                              ).filter(Course.Category.ilike(f'%{inp}%')).all()

            elif sel == "llm_score":
                llm_score = int(inp)
                if 0 <= llm_score <= 5:
                    # Match LLN scores directly
                    results = db.session.query(
                        Course.Category,
                        Course.CName,
                        Course.CNumber,
                        AssignQ.Qid,
                        AssignQ.QText,
                        AssignQ.VText,
                        LLM_Answer.AnswerID,
                        LLM_Answer.LLM_Score
                    ).join(AssignQ, Course.CNumber == AssignQ.CNumber
                           ).join(LLM_Answer, AssignQ.Qid == LLM_Answer.Qid
                                  ).filter(LLM_Answer.LLM_Score == llm_score).all()
                else:
                    return render_template('searchTeacher.html')
            else:
                return render_template('searchTeacher.html')
            print(results)
            return render_template('searchResults.html', results=results)
    else:
        return redirect(url_for('user.login'))


# The teacher gets the details of the problem
@searchTeacherBP.route('/qid:<qid>', methods=['GET', 'POST'])
def get_detail(qid):
    Uid = session.get('Uid')
    if Uid:
        print(qid)
        results = db.session.query(
            AssignQ.Qid,
            LLM_Answer.AnswerID,
            AssignQ.QText,
            AssignQ.VText,
            LLM_Answer.LLM_Name,
            LLM_Answer.LLMAnswerImg,
            LLM_Answer.LLM_Score
        ).join(LLM_Answer, AssignQ.Qid == LLM_Answer.Qid
               ).filter(AssignQ.Qid == qid).all()
        new_results = []
        import base64
        for re in results:
            img_stream = ''
            with open(re.LLMAnswerImg, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()

            new_results.append({
                'Qid': re.Qid,
                'AnswerID': re.AnswerID,
                'QText': re.QText,
                'VText': re.VText,
                'LLM_Name': re.LLM_Name,
                'LLMAnswerImg': img_stream,
                'LLM_Score': re.LLM_Score
            })
        # print(results)
        return render_template('questionDetail.html', results=new_results, qid=qid)
    else:
        return redirect(url_for('user.login'))

# Teacher check comment.
@searchTeacherBP.route('/aid:<aid>', methods=['GET', 'POST'])
def get_comment(aid):
    Uid = session.get('Uid')
    if Uid:
        print(aid)
        results = LLM_Answer.query.filter(LLM_Answer.AnswerID == aid).first()
        import base64
        img_stream = ''
        with open(results.LLMAnswerImg, 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream).decode()
        results.LLMAnswerImg = img_stream
        print(results)
        return render_template('getComment.html', results=results)
    else:
        return redirect(url_for('user.login'))


# Go to the save function
@searchTeacherBP.route('/save_qid:<qid>', methods=['GET', 'POST'])
def save_qid(qid):
    print("qid:", qid)
    return redirect(url_for('SearchTeacher.saveExperiment', id=qid))


# The teacher's save.
@searchTeacherBP.route('/saveExperiment/<id>/', methods=['POST', 'GET'])
def saveExperiment(id):
    Uid = session.get('Uid')
    if Uid:
        print("id ", id)
        if request.method == 'GET':
            return render_template('saveExperiment.html', qid=id)
        else:
            qid = request.form.get('qid')
            vtext = request.form.get('vtext')
            llm_name = request.form.get('llm_name')
            llm_solution = request.values.get('llm_solution')
            llm_score = request.values.get('llm_score')
            print(Uid, qid, vtext, llm_solution, llm_score)
            with db.auto_commit():
                New_exp = Save(uid=Uid, qcode=qid, q_text=vtext, llm_name=llm_name, llmanswerImg=llm_solution,
                               llm_score=llm_score)
                db.session.add(New_exp)
            return render_template('check_save_tea.html', qid=qid, q_text=vtext, llm_name=llm_name,
                                   llmanswerImg=llm_solution, llm_score=llm_score)
    else:
        return redirect(url_for('user.login'))


# add question_test(q_test) llm_solution llm_score Uid
# llm_name CNumber QCode
# to save

# change score change score.html
# add Uid aid new_score explanation
# to request
@searchTeacherBP.route('/changescore_jump:<aid>/', methods=['GET', 'POST'])
def jump_score(aid):
    uid = session.get('Uid')
    print("aid: ", aid)
    print("uid: ", uid)
    return redirect(url_for('SearchTeacher.add_score', id=aid))


@searchTeacherBP.route('/add_score/<id>/', methods=['GET', 'POST'])
def add_score(id):
    print("aid: ", id)
    uid = session.get('Uid')
    print("uid: ", uid)
    if uid:
        if request.method == 'GET':
            return render_template('Change_Score.html', aid=id)
        else:
            aid = request.form.get('aid')
            score = request.form.get('score')
            explain = request.form.get('explain')

            with db.auto_commit():
                New_score = ChangeScore(uid=uid, aid=aid, explanation=explain, score=score)
                db.session.add(New_score)
            # time.sleep(5)  # To simulate waiting for five seconds.
            # return 'experiment save successfully'
            return render_template('check_score_tea.html', uid=uid, aid=aid, explanation=explain, score=score)
            # return redirect(url_for('SearchTeacher.add_score', id=aid)) 
    else:
        return redirect(url_for('user.login'))


# add new course,newCourse.html
@searchTeacherBP.route('/add_course', methods=['POST', 'GET'])
def add_course():
    uid = session.get('Uid')
    print("uid: ", uid)
    if uid:
        if request.method == 'GET':
            return render_template('addCourse.html', title='Sample Login', header='Sample Case')
        else:
            cName = request.form.get('CName')
            Explain = request.form.get('Explain')
            cat = request.values.get('selectcate')
            print(cName, Explain, cat)
            result = AddCourse.query.filter(and_(AddCourse.CourseName == cName, AddCourse.Explanation == Explain,
                                                 AddCourse.Category == cat)).first()

            print(result)
            if result:
                return render_template('login.html', title='Sample Login', header='you have email or password')
            else:
                with db.auto_commit():
                    New_Course = AddCourse(coursename=cName, explanation=Explain, category=cat)
                    db.session.add(New_Course)
                # time.sleep(5)  # To simulate waiting for five seconds

                return render_template('check_addcourse_tea.html', coursename=cName, explanation=Explain, category=cat)
                # return redirect(url_for('SearchTeacher.add_course'))
    else:
        return redirect(url_for('user.login'))


# save history,saveHistory.html
# To view all your saved content, click on the title to open the details
@searchTeacherBP.route('/save_history', methods=['GET', 'POST'])
def save_history():
    uid = session.get('Uid')
    print(uid)
    if uid:
        results = Save.query.filter(Save.Uid == uid).all()
        import base64
        for r in results:
            img_stream = ''
            with open(r.LLMAnswerImg, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
            r.LLMAnswerImg = img_stream
        print(results)
        return render_template('Save_History.html', results=results)
    else:
        return redirect(url_for('user.login'))


# experiment detail ,experimentdetail.html,
# Click the button to open the topic details, and click "submit" to submit to the Request
@searchTeacherBP.route('/sid:<Sid>', methods=['POST', 'GET'])
def save_submit(Sid):
    print(Sid)
    uid = session.get('Uid')
    print(uid)
    if uid:
        results = Save.query.filter(Save.Sid == Sid).first()
        with db.auto_commit():
            New_experiment = AddExperiment(vtext=results.Q_Text, llmanswerImg=results.LLMAnswerImg,
                                           qcode=results.QCode, score=results.LLM_Score)

            db.session.add(New_experiment)
        print(results)

        return redirect(url_for('SearchTeacher.save_history'))
    else:
        return redirect(url_for('user.login'))
