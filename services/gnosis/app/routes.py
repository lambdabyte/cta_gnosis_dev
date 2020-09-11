from app import app
from app import db
import os
import sys
from app.models import User, Subject, Task, usersubjects
from app.forms import RegistrationForm, LoginForm, SubjectForm, TaskForm
from flask_restx import Resource
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, json, jsonify
from werkzeug.urls import url_parse
from sqlalchemy import text
from .clients import Dynamo_Client
from .utilities import JSON_Decimal_Encoder, Dict_FloatsToDecimals
from .views.view_templates import API_View
from datetime import datetime
import base64
import boto3
import werkzeug


class HealthCheck_View(API_View):

    def __init__(self):
        pass

    def get(self):
        return self.get_json_response(
            ({'success':True}), 
            200, 
            {'ContentType':'application/json'}
        )

# urls for health check API
healthcheck_api_view = HealthCheck_View.as_view('health_check')
app.add_url_rule('/health_check/', view_func = healthcheck_api_view, methods=["GET",])

@app.route('/')
@app.route('/home')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.entered_username.data, email=form.entered_email.data)
        user.set_password(form.entered_password.data)
        add_record_to_db(user)
        login_user(user)
        return redirect('user/' + current_user.username)
    return render_template('register.html', title='Register', form=form)

def add_record_to_db(model):
    db.session.add(model)
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
    subjects =  user.subjects
    client = Dynamo_Client()
    plans = client.list_userplan_names(str(user.id))
    user_subjects_select_sql = text(
        ' SELECT subject_id, user_id, subject_description, color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID'
    )
    user_subjects_query = db.engine.execute(user_subjects_select_sql, userID=user.id)
    subject_descriptions = {row[0]:{'description': row[2], 'color': row[3]} for row in user_subjects_query}
    return render_template('user.html', user=user, subjects=subjects, plans=plans, subject_descriptions=subject_descriptions)

@app.route('/list_users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

@app.route('/user/<username>/add_profession', methods=['GET', 'POST'])
@login_required
def add_profession(username):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    profession = request.form['profession']
    user.profession = profession
    db.session.commit()
    return redirect(url_for('user', username=user.username))

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
    # check if subject 
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
    dynamo_client = Dynamo_Client()
    subjects =  current_user.subjects
    graph_loaded = ""
    args = request.args
    if args:
        graph_loaded = dynamo_client.get_userplan(args['user'], args['plan'])
    filenames = dynamo_client.list_userplan_names(str(current_user.id))
    user_subjects_select_sql = text(
        ' SELECT subject_id, user_id, subject_description, color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID'
    )
    user_subjects_query = db.engine.execute(user_subjects_select_sql, userID=current_user.id)
    subject_descriptions = {row[0]:{'description': row[2], 'color': row[3]} for row in user_subjects_query}
    return render_template('goals.html', subjects=subjects, subject_descriptions=subject_descriptions, filenames=filenames, graph_loaded=graph_loaded)

@app.route('/list_plans', methods=['GET'])
@login_required
def list_plans():
    dynamo_client = Dynamo_Client()
    plan_list = dynamo_client.list_userplan_names(str(current_user.id))
    response = {'plan_list': plan_list}
    return json.dumps(response)

@app.route('/load_graph', methods=['GET', 'POST'])
@login_required
def load_graph():
    dynamo_client = Dynamo_Client()
    plan_to_load = request.args.get('plan_to_load', 0, type=str)
    if request.args.get('user_id', 0, type=int):
        user_id = request.args.get('user_id', 0, type=int)
    else:
        user_id = current_user.id
    plan_data = dynamo_client.get_userplan(str(user_id), plan_to_load)
    # Get plan name from query
    plan_name = plan_data['plan_name']
    # Remove plan name and user id from data for clean chart load
    del plan_data['plan_name']
    del plan_data['user_id']
    # Format response
    response = {'plan_data': plan_data, 'plan_name': plan_name}
    return json.dumps(response, cls=JSON_Decimal_Encoder)

@app.route('/save_graph', methods=['GET', 'POST'])
@login_required
def save_graph():
    dynamo_client = Dynamo_Client()
    data = request.json
    graph = data['plan_graph']
    plan_name = data['plan_name']
    plan_description = data['plan_description']
    # New dynamoDB storage
    graph_json = json.loads(graph)
    recursive_float_decimal_parser = Dict_FloatsToDecimals()
    recursive_float_decimal_parser.recursive_float_to_decimal(graph_json)
    graph_start = {
        'user_id': str(current_user.id), 
        'plan_name': plan_name,
        'plan_description': plan_description
    }
    graph_final = {**graph_start, **graph_json}
    userplan_exists = dynamo_client.check_userplan_exists(
        str(current_user.id), plan_name)
    if userplan_exists == False: 
        dynamo_client.put_item_in_table(graph_final, 'gnosis_user_plans')
        msg = plan_name + ' saved.'
        response = jsonify(
            message=msg,
            saved=1
        )
    else:
        msg = plan_name + ' alread exists. Overwrite plan?'
        response = jsonify(
            message=msg,
            saved=0
        )
    return response
    
@app.route('/overwrite_graph', methods=['GET', 'POST'])
@login_required
def overwrite_graph():
    dynamo_client = Dynamo_Client()
    data = request.json
    graph = data['plan_graph']
    plan_description = data['plan_description']
    plan_name = data['plan_name']
    # New dynamoDB storage
    graph_json = json.loads(graph)
    recursive_float_decimal_parser = Dict_FloatsToDecimals()
    recursive_float_decimal_parser.recursive_float_to_decimal(graph_json)
    graph_start = {
        'user_id': str(current_user.id), 
        'plan_name': plan_name,
        'plan_description': plan_description
    }
    graph_final = {**graph_start, **graph_json}
    dynamo_client.put_item_in_table(graph_final, 'gnosis_user_plans')
    msg = plan_name + ' saved.'
    response = jsonify(message=msg)
    return response

@app.route('/delete_graph', methods=['POST'])
@login_required
def delete_graph():
    dynamo_client = Dynamo_Client()
    plan_to_delete = request.form['planval']
    dynamo_client.delete_item(current_user.id, plan_to_delete, 'gnosis_user_plans')
    return redirect(url_for('goals'))


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    user = current_user
    subjects =  user.subjects    
    user_subjects_select_sql = text(
        ' SELECT subject_id, user_id, subject_description, color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID'
    )
    task_info_select_sql = text(
        ' SELECT color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID '
        ' AND subject_id = :subjectID '
    )
    tasks = user.tasks
    task_color = {}
    task_subjects = {}
    user_subjects_query = db.engine.execute(user_subjects_select_sql, userID=user.id)
    subject_descriptions = {row[0]:{'description': row[2], 'color': row[3]} for row in user_subjects_query}
    if len(tasks) > 0:
        for task in tasks:
            task_info_query = db.engine.execute(task_info_select_sql, userID=user.id, subjectID=task.subject_id)
            task_color[task.task_name] = task_info_query.fetchone()[0]
            for subject in subjects:
                if subject.id == task.subject_id:
                    task_subjects[task.task_name] = subject.subject_name
    if len(subjects) > 0:
        form.subjects.choices = []
        for subject in subjects:
            form.subjects.choices.append((subject.id, subject.subject_name))
    return render_template('tasks.html', subjects=subjects, subject_descriptions=subject_descriptions, form=form, tasks=tasks, task_color=task_color, task_subjects=task_subjects)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    task_title = request.form['title']
    subject_id = request.form['subjects']
    due_date = request.form['date']
    task_description  = request.form['description']
    task = Task(
        task_name=task_title, 
        due_date=due_date,
        task_description=task_description,
        subject_id=subject_id,
        user_id=current_user.id
        )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/edit_task', methods=['POST'])
@login_required
def edit_task():
    task_title = request.form['title']
    due_date = request.form['date']
    task_description  = request.form['description']
    task_id = request.form['taskid']
    update_task_sql = text(
        ' UPDATE task SET task_name = :task_title, due_date = :due_date, task_description = :task_description '
        ' WHERE  id = :task_id'
    )
    db.engine.execute(
        update_task_sql,
        task_title = task_title,
        due_date = due_date,
        task_description = task_description,
        task_id = int(task_id)
    )
    return redirect(url_for('tasks'))

@app.route('/delete_task', methods=['GET', 'POST'])
@login_required
def delete_task():
    task_id = request.form['taskid']
    task_to_delete = Task.query.filter_by(id=task_id).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/notebook', methods=['GET', 'POST'])
@login_required
def notebook():
    notes = []
    order = {}
    s3 = boto3.client('s3')
    notebooks= s3.list_objects(Bucket='gnosis-notebooks')
    for note_folder in notebooks['Contents']: # loop through all the files and folders
        note_folder_name = note_folder['Key'].split('/')
        note_folder_test = note_folder_name[0].split('-')
        if note_folder_test[0] == str(current_user.id):
            order[note_folder_test[1]] = []
            note_name = note_folder_name[1].split('-')[1].split('.')[0]
            order[note_folder_test[1]].append(note_name)
            notes.append({'subject': note_folder_test[1], 'note': note_name})
    order = json.dumps(order)
    user = current_user
    subjects =  user.subjects    
    user_subjects_select_sql = text(
        ' SELECT subject_id, user_id, subject_description, color '
        ' FROM usersubjects '
        ' JOIN subject ON (subject.id = usersubjects.subject_id) '
        ' JOIN "user" ON ("user".id = usersubjects.user_id) '
        ' WHERE user_id = :userID'
    )
    test_notes = ['note', 'two', 'three', 'notefour']
    user_subjects_query = db.engine.execute(user_subjects_select_sql, userID=user.id)
    subject_descriptions = {row[0]:{'description': row[2], 'color': row[3]} for row in user_subjects_query}
    return render_template('notebook.html', subjects=subjects, subject_descriptions=subject_descriptions, note_titles=test_notes, notes=notes, order=order)

@app.route('/new_notepad', methods=['GET', 'POST'])
@login_required
def new_notepad():
    if request.method == 'POST':
        if request.form['notepad']:
            s3 = boto3.client('s3')
            notepad_write = str(current_user.id) + '-' + request.form['notepadhead']
            notepad_sub = str(current_user.id) + '-' + request.form['notepadsub']
            notepad = request.form['notepad']
            whole_path = notepad_sub + '/' + notepad_write + '.txt'
            s3.put_object(Body=notepad, Bucket='gnosis-notebooks', Key=(whole_path))
    return redirect(url_for('notebook'))

@app.route('/new_notes', methods=['GET', 'POST'])
@login_required
def new_notes():
    if request.form['newnote']:
        s3 = boto3.client('s3')
        note = request.form['newnote']
        note_subject = request.form['notesubject']
        notebook_name = str(current_user.id) + '-' + note_subject + '/' + str(current_user.id) + '-' + note + '.txt'
        s3.put_object(Bucket='gnosis-notebooks', Key=(notebook_name))
    return redirect(url_for('notebook'))
        

@app.route('/get_notes', methods=['GET', 'POST'])
@login_required
def get_notes():
    note = request.args.get('note', 0, type=str)
    subject = request.args.get('sub', 0, type=str)
    s3 = boto3.client('s3')
    key = str(current_user.id) + '-' + subject + '/' + str(current_user.id) + '-' + note + '.txt'
    obj = s3.get_object(Bucket='gnosis-notebooks', Key=key)
    try:
        data = obj['Body'].read().decode('utf-8')
    except Exception as e:
        raise werkzeug.exceptions.HTTPException("Error: %s" % str(e) )
    order = {'note': data}
    return jsonify(result=order)

@app.route('/delete_note', methods=['GET', 'POST'])
@login_required
def delete_note():
    s3 = boto3.client('s3')
    note_title = request.form['note-to-delete']
    subject = request.form['note-to-delete-subject']
    note_key = str(current_user.id) + '-' + subject + '/' + str(current_user.id) + '-' + note_title + '.txt'
    response = s3.delete_object(Bucket='gnosis-notebooks', Key=note_key)
    return redirect(url_for('notebook'))

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }