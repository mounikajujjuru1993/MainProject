#from werkzeug import secure_filename

from dataclasses import dataclass
from email.mime import application
from math import remainder
import re
from ssl import Purpose
from traceback import StackSummary
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
import os
from flask.globals import current_app
from flask.helpers import send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from datetime import datetime,timedelta
import base64
from flask_sqlalchemy import SQLAlchemy

from apps import Base_URL
from models import *


def commit_data(data):
    db.session.add(data)
    db.session.commit()   


@app.route('/',methods =["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method== "POST":
        username=request.form["username"]
        pass_code=request.form["pass"]
        person=db.session.query(Applicants).filter(Applicants.username==username).first()
        print(person.username)
        if db.session.query(Applicants).filter(Applicants.username==username).count()!=0:

            if person.passcode==pass_code:
                session["email"]=person.email
                print(session["email"])
                return redirect('/dashboard')
            else:
                flash("Email or Password not correct!")
        else:
            flash("You dont have an account!")
            return redirect('/signup')
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'email' in session:  
        session.pop('email',None)  
        return redirect("/login")  
    else:  
        my_message='You are loogged out sucessfully.'
        link='login'
        link_data="Log in"
        return render_template("activate.html", my_message=my_message,link=link,link_data=link_data)
                



@app.route('/signup',methods =["GET","POST"])
def signup():
    if request.method== "POST":
        email_string=request.form["email"]
        phone=request.form["phone"]
        username = request.form["uname"]  
        sep= request.form["sep"] 
        type_app=request.form.get('type')
        #add a fetch all to chech for emails and phone duplication
        root_pass=request.form["passcode"]
        repeat_pass=request.form["repeatpassword"] 
        reg=request.form["reg"] 

        print(email_string)

        if root_pass != repeat_pass:
            flash('Passwords Do not match')
        else:
            if len(root_pass)<8:
                flash("Your Password should be more than 8 Characters")
            else:
                if db.session.query(Applicants).filter(Applicants.username==username).count()!=0:
                    flash("Username exists. Choose another.")
                else:
                    #r_code=generate_refer_code(mail,phone)
                    if db.session.query(Applicants).filter(Applicants.email==email_string).count()!=0:
                        flash("Account with that email already exists.")
                    else:
                        if len(phone)!=12:
                            flash("Phone number is incorrect. Format is: +44XXXXXXXX")
                        else:
                            
                            create_users=Applicants(email=email_string,phone=phone,passcode=root_pass,username=username,security_question =sep,security_phrase=sep,type_app=type_app,registration=reg)
                            commit_data(create_users)
                            my_message="Account created Successfully!"
                            
                            link='login'
                            link_data="Log In"
                            return render_template("activate.html", my_message=my_message,link=link,link_data=link_data) 
    return render_template('signup.html')

@app.route('/apply',methods =["GET","POST"])
def apply():
    if request.method== "POST":
        if session['email']==None or session['email']=="":
            my_message= 'You are Logged out.'
            link='login'
            link_data="Log In"
            return render_template("activate.html", my_message=my_message,link=link,link_data=link_data)
            
        else:
            purpose=request.form['pres']
            sum_requested=request.form['sum_requested']
            add_infor=request.form['infor']
            print(session['email'])

            appli=db.session.query(Applications).filter(Applications.status=='1' and Applications.owner==session['email'])
            print(appli.count())
            if appli.count()==1:
                my_message='You have a pending application. You will be notified when a response is available.'
                link='dashboard'
                link_data="View Dashboard"
                return render_template("activate.html", my_message=my_message,link=link,link_data=link_data)
                
            else:
                send_application=Applications(purpose,session['email'],'1',sum_requested,add_infor)
                commit_data(send_application)
                my_message='Application has been sent.'
                link='dashboard'
                link_data="View Dashboard"
                return render_template("activate.html", my_message=my_message,link=link,link_data=link_data) 

    return render_template('apply.html')

@app.route('/dashboard',methods =["GET","POST"])
def dashboard():
    
    if "email" not in session:
        my_message= 'You are Logged out.'
        link='login'
        link_data="Log In"
        return render_template("activate.html", my_message=my_message,link=link,link_data=link_data)
    else:
        appn_records= db.session.query(Applications).filter(Applications.owner==session['email'])
        appt=db.session.query(Applicants).filter(Applicants.email==session['email'])
        total_apps=appn_records.count()
        approved=db.session.query(Applications).filter(Applications.owner==session['email'] and Applications.status=='2').count()
        declined=total_apps-approved
        if total_apps ==0:
            success_rate = "No applications yet"
        else:
            success_rate=round(((approved/total_apps) * 100),0)
        pending=db.session.query(Applications).filter(Applications.owner==session['email'] and Applications.status=='1').count()
        

    return render_template('dashboard_home.html',pending=pending,appn_records=appn_records.all(),success_rate=success_rate,approved=approved,total_apps=total_apps,declined=declined,mail=session['email'])
    


@app.route('/admin',methods =["GET","POST"])
def admin_login():
    if request.method=='POST':
        username=request.form["username"]
        pass_code=request.form["pass"]
        admin=db.session.query(Admin).filter(Admin.username==username).first()
        if username!=admin.username:
            flash("Email or password incorrect!")
        if admin.password_string==pass_code:
            session['username'] = admin.username
            return redirect('admin_dashboard')
        else:
            flash("Email or password incorrect!")
    return render_template('admin_login.html')




@app.route('/admin_dashboard',methods =["GET","POST"])
def admin_dashboard():
    appn_records= db.session.query(Applications)
    approval = db.session.query(Application_approved).filter(Application_approved.approver==session['username']).all()
    
    


    approved=0#appn_records.filter(Applications.status=='2' and Applications.id==approval.id ).count()
    declined = 0#appn_records.filter(Applications.status=='3' and Applications.id==approval.id ).count()
    total_apps = 0#approved + declined
    success_rate=0#(approval * 100) / (total_apps)



    return render_template('admin_dashboard.html',mail=session['username'],appn_records=appn_records.all(),approved=approved,declined=declined,total_apps=total_apps,success_rate=success_rate)

@app.route('/approve/<pur>/<sum_req>/<information>/<id>',methods =["GET","POST"])
def approve(pur,sum_req,information,id):
    if request.method == "GET":
        if id:
            identity=id
            
        if pur:
            purposes=pur
        else:
            purposes="NULL"
        if sum_req:
            s=sum_req
        else:
            s="NULL"
        if information:
            inform=information
        else:
            inform="NULL"
        
        return render_template('approve.html',purpose=purposes,infor=inform,sum_requested=s)
        
    if request.method == "POST":
        
            
        if pur:
            purposes=pur
        else:
            purposes="NULL"
        if sum_req:
            s=sum_req
        else:
            s="NULL"
        if information:
            inform=information
        else:
            inform="NULL"
        if id:
            identity=int(id)
            
            ap=db.session.query(Applications).filter(Applications.id==identity).first()
            
        
            if request.form['btnCapture'] == 'Approve':
                print(ap.owner)
                if ap.status not in ['2','3']:
                    ap.status='2'
                    db.session.commit()
                    flash("Application approved!")
                else:
                    flash('This application has been processed!')
            else:
                if ap.status not in ['2','3']:
                    ap.status='3'
                    db.session.commit()
                    flash("Application declined!")
                else:
                    flash('This application has been processed!')

                

    return render_template('approve.html',purpose=purposes,infor=inform,sum_requested=s)

@app.route('/activate',methods =["GET","POST"])
def activate():
    return render_template('activate.html')


    