from flask import Flask
from app.controller import SearchStudent, SearchTeacher,user,RequestAdmin

# Define the registration blueprint method
def register_blueprints(app):
    app.register_blueprint(user.userBP,url_prefix='/user')
    app.register_blueprint(SearchTeacher.searchTeacherBP,url_prefix='/SearchTeacher')
    app.register_blueprint(SearchStudent.searchStudentBP, url_prefix='/SearchStudent')

    # 
    app.register_blueprint(RequestAdmin.RequestBP, url_prefix='/RequestAdmin')
    # app.register_blueprint(New_Course.NewCourseBP, url_prefix='/NewCourse')
    # app.register_blueprint(New_Experiment.NewExperimentBP, url_prefix='/NewExperiment')

# Register plugins (database association).
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    # create all is meant to be used in an app context
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    # app.config.from_object('app.config.setting') # Basic configuration (setting.py)
    app.config.from_object('app.config.secure') # Important parameter configuration (secure.py)
    # The registration blueprint is associated with the app object
    register_blueprints(app)
    # The registration plugin (database) is associated with the app object
    register_plugin(app)
    # Always remember to return to the app
    return app