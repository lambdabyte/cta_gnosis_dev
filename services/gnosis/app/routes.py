from app import app
from app import db
from app.models import User, Subject, usersubjects
from app.forms import RegistrationForm, LoginForm, SubjectForm
from flask_restx import Resource
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from sqlalchemy import text

@app.route('/index')
def home():
    return render_template('index.html')


"""
User Viewss
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.entered_username.data, email=form.entered_email.data)
        user.set_password(form.entered_password.data)
        add_user_to_database(user)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

def add_user_to_database(user):    
    db.session.add(user)
    db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # set user valid for error msg
    valid_user = 1;
    if form.validate_on_submit():
        # get User from database based on entered user
        user = User.query.filter_by(username=form.entered_username.data).first()
        # if user does not exist, or wrong password
        if user is None or not user.check_password(form.entered_password.data):
            valid_user = 0;
        else:
            login_user(user, remember=form.remember_me.data)
            # get current page       
            next_page = request.args.get('next')
            # if no next page, redirect to home
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            # else return to user to originally requested page
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, valid_user=valid_user)
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


"""
Subject Views
"""

@app.route('/subjects', methods=['GET', 'POST'])
@login_required
def subjects():
    user = current_user
    subjects =  user.subjects
    form = SubjectForm()
    user_subjects_select_sql = text(
        ' SELECT subject_id, user_id, subject_description, color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID'
    )
    user_subjects_query = db.engine.execute(user_subjects_select_sql, userID=user.id)
    subject_descriptions = {row[0]:{'description': row[2], 'color': row[3]} for row in user_subjects_query}
    if form.validate_on_submit():
        subject = Subject(subject_name=form.title.data)
        i_color = form.color.data
        i_color = i_color.hex_l
        existant_subject = Subject.query.filter_by(subject_name=form.title.data).first()
        insert_statement = text(
            "INSERT INTO usersubjects "
                "VALUES (:user_id, :subject_id, :color, :subject_description);"
            )
        if existant_subject:
            db.engine.execute(
                insert_statement, 
                user_id=user.id,
                subject_id=existant_subject.id, 
                subject_description=form.subject_description.data,
                color=i_color
            )
        else:
            db.session.add(subject)
            db.session.commit()
            db.engine.execute(
                insert_statement, 
                user_id=user.id,
                subject_id=subject.id,
                subject_description=form.subject_description.data,
                color=i_color
            )
            
        return redirect(url_for('subjects'))
    return render_template('subjects.html', subjects=subjects, form=form, subject_descriptions=subject_descriptions)

@app.route('/delete_subject', methods=['POST'])
@login_required
def delete_subject():
    subject_to_delete = request.form['subjectname']
    user_obj = User.query.filter_by(id=current_user.id).first()
    subject_obj = Subject.query.filter_by(id=subject_to_delete).first()
    user_obj.subjects.remove(subject_obj)
    db.session.commit()
    # Check if other users have subject before deleting from main subjects
    user_subjects_check_sql = text(' SELECT subject_id FROM usersubjects WHERE subject_id = :subjectID ') 
    user_subjects_check = db.engine.execute(user_subjects_check_sql, subjectID=subject_to_delete)
    subject_has_other_users=False
    for row in user_subjects_check:
        if row[0] == int(subject_to_delete):
            subject_has_other_users = True
    if subject_has_other_users == False:
        Subject.query.filter_by(id=subject_to_delete).delete()
        db.session.commit()
    return redirect(url_for('subjects'))

@app.route('/edit_subject', methods=['POST'])
@login_required
def edit_subject():
    subject_to_edit = request.form['subjectid']
    subject_description = request.form['subjectdescription']
    subject_color = request.form['subjectcolor']
    update_user_subject_sql = text(
        ' UPDATE usersubjects SET subject_description = :subject_description, color = :subject_color '
        ' WHERE user_id = :user_id AND subject_id = :subject_id'
    )
    db.engine.execute(update_user_subject_sql, subject_description=subject_description, subject_color=str(subject_color), user_id=current_user.id, subject_id=int(subject_to_edit))
    return redirect(url_for('subjects'))

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    user = current_user
    subjects =  user.subjects
    user_subjects_select_sql = text(
        ' SELECT subject_id, user_id, subject_description, color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID'
    )
    user_subjects_query = db.engine.execute(user_subjects_select_sql, userID=user.id)
    subject_descriptions = {row[0]:{'description': row[2], 'color': row[3]} for row in user_subjects_query}
    return render_template('goals.html', subjects=subjects, subject_descriptions=subject_descriptions)

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }