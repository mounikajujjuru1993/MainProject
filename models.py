from email.mime import application
from apps import app
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    #position = db.Column(db.String())
    username = db.Column(db.String())
    #curent_votes = db.Column(db.Integer)
    password_string=db.Column(db.String())
    
    def __init__(self, username, password_string):
        self.username = username
        self.password_string = password_string


  
class Applicants(db.Model):
    __tablename__ = 'applicants'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    phone = db.Column(db.String())
    passcode = db.Column(db.String())
    username =  db.Column(db.String())
    registration = db.Column(db.String())
    security_question = db.Column(db.String())
    security_phrase = db.Column(db.String())
    type_app = db.Column(db.String())

    def __init__(self, email, phone, passcode,username,security_question,security_phrase,type_app,registration):
        self.email= email
        self.phone = phone
        self.passcode = passcode
        self.registration = registration
        self.username = username
        self.security_question=security_question        
        self.security_phrase=security_phrase 
        self.type_app = type_app     



class Applications(db.Model):
    __tablename__ = 'applications'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    purpose = db.Column(db.String())
    owner = db.Column(db.String())
    status = db.Column(db.String())
    sum_requested = db.Column(db.Integer)
    additional_infor=db.Column(db.String(300))

    def __init__(self,purpose,owner, status,sum_requested,additional_infor,):
        self.purpose = purpose
        self.owner = owner
        self.status = status
        #self.image = image
        self.sum_requested = sum_requested
        self.additional_infor=additional_infor   

class Application_approved(db.Model):
    __tablename__ = 'approved'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))
    approver = db.Column(db.String())
    date_approved = db.Column(db.String())
    

    def __init__(self,application_id,approver ,date_approved,):
        self.application_id = application_id
        self.approver  = approver 
        self.date_approved = date_approved
        


create_admin=Admin('admin','admin123')
db.session.add(create_admin)
db.session.commit() 



















db.create_all()
# create_admin=Admin(username="admin",password_string="admin123")
# db.session.add(create_admin)
# db.session.commit() 

# create_admin_=db.session.query(Voter).filter(Voter.idno=='34194031').first()

# create_admin_.security_question="dog"
# create_admin_.security_phrase="I like mangos"
#db.session.commit() 


