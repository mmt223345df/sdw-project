
from flask import Blueprint, redirect,render_template, request, session, url_for
from sqlalchemy import and_
from app .models .base import db
from app.models.user import User

userBP = Blueprint('user',__name__)

@userBP.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',title='Sample Login',header='Sample Case')
    else:

        email = request.form.get('email')
        _password = request.form.get('password')
        usertype = request.values.get('usertype')
        print(email, _password, usertype)
        
        if usertype=="Student":
            result = User.query.filter(and_(User.Email == email,User._Password == _password,User.UserType == "Student")).first()
            if result:
                print(result)
                session['Uid']=result.Uid
                session['UserType'] = result.UserType
                session.permanent=True
                return redirect(url_for('SearchStudent.search_student'))
        if usertype=="Teacher":
            result = User.query.filter(and_(User.Email == email,User._Password == _password,User.UserType == "Teacher")).first()
            if result:
                print(result)
                session['Uid']=result.Uid
                session['UserType'] = result.UserType
                session.permanent=True
                return redirect(url_for('SearchTeacher.search_teacher'))
        if usertype=="Administer":
            result = User.query.filter(and_(User.Email == email,User._Password == _password,User.UserType == "Administer")).first()
            if result:
                print(result)
                session['Uid']=result.Uid
                session['UserType'] = result.UserType
                session.permanent=True  
                return redirect(url_for('RequestAdmin.Request'))
        
        else:
            return render_template('login.html',title='Sample Login',header='you have error email or password')

@userBP.context_processor
def my_context_processor():
    Uid=session.get('Uid')
    print(Uid)
    if Uid:
        return {'Uid':Uid}
    return {}

@userBP.route('/logout/',methods=['POST','GET'])
def logout():

    session.pop('Uid', None)
    session.clear()  # Destroy the entire session object
    # You cannot return to login.html, or the contents of logout will be executed.
    # return 'Logout successful'
    return render_template('logout.html')


@userBP.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Register', header='Sample Case')
    else:

        email = request.form.get('email')
        _password = request.form.get('password')
        usertype = request.values.get('usertype')
        print(email, _password, usertype)
        result = User.query.filter(
            and_(User.Email == email, User._Password == _password, User.UserType == usertype)).first()

    print(result)
    if result:
        return render_template('login.html', title='Sample Login', header='you have email or password')
    else:
        with db.auto_commit():
            teacher = User(email, _password, usertype)
            db.session.add(teacher)
        return redirect(url_for('user.login'))







