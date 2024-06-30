
from flask import Blueprint, render_template, request, redirect, session, url_for

from app.models.addHelptopic import AddHelptopic
from app.models.base import db
from app.models.assignq import AssignQ
from app.models.course import Course
from app.models.llm_answer import LLM_Answer
from sqlalchemy import and_, or_

from app.models.save import Save
from app.models.save_student import Save_stu
from app.models.topic import Topic
from app.models.topicQA import TopicQA

searchStudentBP = Blueprint('SearchStudent', __name__)

#Maintain user information
@searchStudentBP.context_processor
def my_context_processor():
    Uid=session.get('Uid')
    UserType = session.get('UserType')
    print(Uid)
    if Uid:
        return {'Uid': Uid, 'UserType': UserType}
    else:
        return redirect(url_for('user.login'))

#Searchcourse&category student(); return list topic &subtopic
#If you can't find it, you can output it.
@searchStudentBP.route('/search_student', methods=['POST','GET'])
def search_student():
    Uid=session.get('Uid')
    if Uid:
        if request.method == 'GET':
            return render_template('searchStudent.html')
        else:
            sel = request.values.get('searchstu')
            inp = request.form.get("searchstuin")
            print(sel, inp)

            if sel == "course_name_number":
                CNumber = inp
                CName = inp
                results = db.session.query(
                    Course.Category,
                    Course.CName,
                    Course.CNumber,
                    Topic.Tid,
                    Topic.Topic_name,
                    Topic.SubTopic_name
                ).join(Topic, Course.CNumber == Topic.CNumber
                ).filter(or_(Course.CNumber == CNumber, Course.CName == CName)).all()

            elif sel == "course_category":
                category = inp

                results = db.session.query(
                    Course.Category,
                    Course.CName,
                    Course.CNumber,
                    Topic.Tid,
                    Topic.Topic_name,
                    Topic.SubTopic_name
                ).join(Topic, Course.CNumber == Topic.CNumber
                ).filter(Course.Category == category).all()
            else:
                return render_template('searchStudent.html')
            print(results)
            return render_template('searchResults_stu.html', results=results)
    else:
        return redirect(url_for('user.login'))

#topic detail
#topicDetail.html
#Displays the LLM used, the LLM hint for the request explanation, the LLM answer,
#and the degree to which the LLM answer was helpful
#If SubTopic_name has a value, it is displayed. Otherwise, Topic_name is displayed
#If there is no answer to the question, skip it
@searchStudentBP.route('/tid:<tid>',methods=['GET','POST'])
def get_detail_stu(tid):
    Uid=session.get('Uid')
    if Uid:
        print(tid)
        results = db.session.query(
            TopicQA.Hid,
            TopicQA.LLM_Name,
            TopicQA.LLM_Prompt,
            TopicQA.PromptAnswerImg,
            TopicQA.Help_score,
            Topic.Topic_name,
            Topic.SubTopic_name
        ).join(TopicQA, Topic.Tid == TopicQA.Tid
        ).filter(Topic.Tid == tid).all()
        gettopic = Topic.query.filter(Topic.Tid == tid).first()

        new_results = []
        import base64
        for re in results:
            img_stream = ''
            with open(re.PromptAnswerImg, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()

            new_results.append({
                'Hid': re.Hid,
                'LLM_Name': re.LLM_Name,
                'LLM_Prompt': re.LLM_Prompt,
                'PromptAnswerImg': img_stream,
                'Help_score': re.Help_score,
                'Topic_name': re.Topic_name,
                'SubTopic_name': re.SubTopic_name
            })

        print(results)
        return render_template('helptopicDetail.html', results=new_results,tid=tid,gettopic=gettopic)

    else:
        return redirect(url_for('user.login'))


#Go to the save function
@searchStudentBP.route('/save_tid:<tid>',methods=['GET','POST'])
def save_qid(tid):
    print("tid:",tid)
    return redirect(url_for('SearchStudent.saveHelptopic', id=tid))

# #Save();
#saveTopic.html        llm_name,llm_prompt,PromptAnswerImg,score
@searchStudentBP.route('/saveHelptopic/<id>/',methods=['POST','GET'])
def saveHelptopic(id):
    Uid=session.get('Uid')
    print("id ",id)
    if Uid:
        if request.method == 'GET':
            return render_template('saveHelptopic.html',tid=id)
        else:
            tid = request.form.get('tid')
            llm_name = request.form.get('llm_name')
            llm_prompt = request.form.get('llm_prompt')
            PromptAnswerImg = request.values.get('PromptAnswerImg')
            score = request.values.get('llm_score')

            print(Uid,tid,llm_prompt,PromptAnswerImg,score)

            with db.auto_commit():
                New_hel = Save_stu(uid=Uid,tid=tid,llm_name=llm_name,llm_prompt=llm_prompt,promptanswerImg=PromptAnswerImg,help_score=score)
                db.session.add(New_hel)
            return render_template('check_save_stu.html',tid=tid,name=llm_name,prompt=llm_prompt,PromptAnswer=PromptAnswerImg,score=score)
            #return redirect(url_for('SearchStudent.saveHelptopic', id=tid))
    else:
        return redirect(url_for('user.login'))




# save help history()
#save_Stuhistory.html
#check helptopic.  llm_name,llm_prompt,PromptAnswerImg,score。
#If there is no information in save, go to that page.
@searchStudentBP.route('/savehelp_history',methods=['GET','POST'])
def save_history():
    uid=session.get('Uid')
    print(uid)
    if uid:
        results = Save_stu.query.filter(Save_stu.Uid == uid).all()
        import base64
        for re in results:
            img_stream = ''
            with open(re.PromptAnswerImg, 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = base64.b64encode(img_stream).decode()
            re.PromptAnswerImg = img_stream
        print(results)
        return render_template('Savehelp_History.html', results=results)
    else:
        return redirect(url_for('user.login'))

#submit in save
@searchStudentBP.route('/sid:<Sid>', methods=['POST','GET'])
def save_submit(Sid):
    uid=session.get('Uid')
    print(uid)
    if uid:
        print(Sid)
        results = Save_stu.query.filter(Save_stu.Sid == Sid).first()
        with db.auto_commit():
            New_experiment = AddHelptopic(tid=results.Tid,llm_prompt=results.LLM_Prompt,promptanswerImg=results.PromptAnswerImg,score=results.Help_score)

            db.session.add(New_experiment)
        print(results)
        return redirect(url_for('SearchStudent.save_history'))
    else:
        return redirect(url_for('user.login'))