from flask import render_template, request, redirect, url_for, session, logging, flash
from server import app, system, user_manager
from flask_login import current_user, login_required, login_user, logout_user, login_manager
from model.client import Staff, Student, User
from model.Event import Course, Seminar, Event, Session
from wtforms import (Form, StringField, TextAreaField, PasswordField, validators,
DateTimeField, DateField, DecimalField, SelectField, IntegerField)
from wtforms.validators import Required
from functools import wraps
from datetime import datetime
from model.UNSW_mem import User, Student, Staff, Guest
from model.Errors import *

@app.route('/login', methods=['GET', 'POST'])
def login():
	zID = None
	password = None

	if request.method == "POST":
		#zID = request.form['zID']
		email = request.form['email']
		password = request.form['password']
		check = user_manager.validate_login(email, password)
		if check is None:
			return render_template('login.html', message='Your zID and password is wrong')
		else:
			login_user(check)
			session['logged_in'] = True
			session['username'] = check.name
			session['staff'] = check.is_Staff()
			session['guest'] = check.is_Guest()
			# print("IS GUEST: ", check.is_Guest())
			flash('You are now logged in', 'success')

			return redirect(url_for('home'))
	return render_template('login.html')

###### GUEST REGISTER #########################
@app.route('/regist3r', methods=['GET', 'POST'])
def regist3r():
	name = None
	email = None
	password = None
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
	#check = user_manager.add_user(Guest(None, name,email,password))
	check = user_manager.add_user(None, name, email, password)
	if check:
		flash("Register Successful", 'success')
	else:
		flash("Email exist - please choose other email", 'danger')
	print(name, email, password)
	return render_template('register.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



@app.route('/')
def index_home():
	return render_template('login.html')


#add course form
##############COURSE############################
@app.route('/add_event', methods=['GET', 'POST'])
@is_logged_in
def add_event():
	form = AddEventForm(request.form)
	date_format = "%Y-%m-%d"
	if request.method == 'POST': #nd form.validate():
		convenor = form.convenor.data
		event = form.event.data
		course_name = form.course_name.data
		location = form.location.data
		duration = form.duration.data
		info = form.info.data

		#date_time = request.form['date_time']
		#print("DATE TIME 1", date_time)
		#date_time = datetime.strptime(str(date_time), date_format)
		#print("DATE TIME ", date_time, type(date_time))
		date_time = form.date_time.data

		early_bird = form.early_bird.data

		print(early_bird)
		print(type(early_bird))

		#date_time = str(datetime.date(date_time))
		capacity = form.capacity.data
		fee = form.fee.data
		poster = session['username']

		coures_id = system.ID_generator()
		try:
		# TRY CATCH  2
			new_event = system.add_course(coures_id, convenor, event, info, course_name, location, date_time, early_bird, duration, poster, capacity,fee)

			if session['staff']:
				staff = user_manager.get_user_by_name(session['username'])
				staff.add_new_post(new_event)

			flash('You added an event to EMS', 'success')
			return redirect(url_for('add_event'))
		except AddEventError as ave:
			#flash('Invalid Date', 'danger')
			return render_template('add_event.html', form=form, errors=ave.errors)
	return render_template('add_event.html', form=form)

# @app.route('/register/<event_name>', methods=['GET', 'POST'])
# @is_logged_in
# def register(event_name):

@app.route('/edit_course/<course_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_course(course_id):
	edit_event = system.get_event_by_ids(course_id)
	form = AddEventForm(request.form, convenor=edit_event.convenor,event=edit_event.event_name,
						course_name=edit_event.course_name,location=edit_event.location,
						capacity= edit_event.capacity, fee=edit_event.fee, duration=edit_event.duration,
						info=edit_event.info, date_time=edit_event.time, early_bird = edit_event.early_bird);
	#date_time=datetime.strptime(edit_event._time, '%d-%m-%Y'
	
	if request.method == 'POST': #nd form.validate():
		try:
			convenor = form.convenor.data
			event = form.event.data
			course_name = form.course_name.data
			location = form.location.data
			duration = form.duration.data
			info = form.info.data
			date_time = form.date_time.data
			early_bird = form.early_bird.data
			capacity = form.capacity.data
			fee = form.fee.data
			errors = check_add_course_error(date_time, early_bird, convenor, event, course_name, location, duration, capacity,fee)
			if errors != {}:
				raise AddEventError(errors)
			edit_event.set_convenor(form.convenor.data)
			edit_event.set_event_name(form.event.data)
			edit_event.set_course_name(form.course_name.data)
			edit_event.set_location(form.location.data)
			edit_event.set_duration(form.duration.data)
			edit_event.set_info(form.info.data)
			edit_event.set_time(form.date_time.data)
			edit_event.set_capacity(form.capacity.data)
			edit_event.set_early_bird(form.date_time.data)
			edit_event.set_fee(form.fee.data)

			flash('You edited a course on EMS', 'success')
			return redirect(url_for('home'))
		except AddEventError as ave:
			return render_template('edit_course.html', form=form, event=edit_event, errors=ave.errors)
	return render_template('edit_course.html', form=form, event=edit_event)


# Register Form Class
# FOR COURSE ONlY
class AddEventForm(Form):
	event = StringField('Event', [validators.Length(min=1, max=50)])
	course_name = StringField('Course Name',[validators.Length(min=1, max=50)])
	convenor = StringField('Convenor', [validators.Length(min=4, max=25)])
	location = StringField('Location', [validators.Length(min=6, max=50)])
	date_time = StringField('Date', validators=[Required()],description='Date format: YYYY-MM-DD')
	early_bird = StringField('Early Bird', validators=[Required()],description='Date format: YYYY-MM-DD')
	capacity = IntegerField('Capacity',[validators.NumberRange(min=1, max=1000)])
	fee = IntegerField('Fee',[validators.NumberRange(min=1, max=1000)])
	duration = DecimalField('Hour', [validators.NumberRange(min=1, max=24)])
	info = TextAreaField('Details about Event', [validators.Length(min=1, max=1000)])

class AddSeminarForm(Form):
	convenor = StringField('Convenor', [validators.Length(min=4, max=25)])
	event_name = StringField('Event Name', [validators.Length(min=1, max=50)])
	event_info=TextAreaField('Event Info', [validators.Length(min=1, max=1000)])
	seminar_name = StringField('Seminar Name',[validators.Length(min=1, max=50)])
	session_location = StringField('Session Location', [validators.Length(min=6, max=50)])
	session_topic = StringField('Session Topic', [validators.Length(min=1, max=50)])
	session_time = StringField('Session Time',validators=[Required()], description='Date format: YYYY-MM-DD')
	early_bird = StringField('Early Bird', validators=[Required()],description='Date format: YYYY-MM-DD')
	session_capacity = IntegerField('Session Capacity',[validators.NumberRange(min=1, max=1000)])
	session_fee = IntegerField('Session Fee',[validators.NumberRange(min=1, max=1000)])
	session_duration = DecimalField('Hour', [validators.NumberRange(min=1, max=24)])

class EditSeminarForm(Form):
	convenor = StringField('Convenor', [validators.Length(min=4, max=25)])
	event_name = StringField('Event Name', [validators.Length(min=1, max=50)])
	event_info = TextAreaField('Event Info', [validators.Length(min=1, max=1000)])
	seminar_name = StringField('Seminar Name',[validators.Length(min=1, max=50)])

class AddSessionForm(Form):
	session_topic = StringField('Session Name', [validators.Length(min=1, max=50)])
	session_location = StringField('Session Location', [validators.Length(min=6, max=50)])
	session_time = StringField('Session Time',validators=[Required()])
	early_bird = StringField('Early Bird', validators=[Required()],description='Date format: YYYY-MM-DD')
	session_capacity = IntegerField('Session Capacity',[validators.NumberRange(min=1, max=1000)])
	session_fee = IntegerField('Session Fee',[validators.NumberRange(min=1, max=1000)])
	session_duration = DecimalField('Hour', [validators.NumberRange(min=1, max=24)])


@app.route('/add_seminar', methods=['GET', 'POST'])
@is_logged_in
def add_seminar():
	form = AddSeminarForm(request.form)
	date_format = "%Y-%m-%d"

	if request.method == 'POST': #nd form.validate():
		convenor = form.convenor.data
		event_name = form.event_name.data
		event_info = form.event_info.data
		seminar_name = form.seminar_name.data
		session_location = form.session_location.data
		session_duration = form.session_duration.data
		session_topic = form.session_topic.data
		#session_time = request.form['session_time']

		#print("SESSION TIME1: ", session_time)
		#session_time = datetime.strptime(str(session_time), date_format)
		#print("SESSION TIME: ", session_time)
		session_time = form.session_time.data
		early_bird = form.early_bird.data
		
		session_capacity = form.session_capacity.data
		session_fee = form.session_fee.data
		poster = session['username']

		seminar_id = system.ID_generator()
		session_id = system.ID_generator()
		try:
			new_seminar = system.add_seminar(session['staff'],seminar_id,convenor, event_name, event_info, seminar_name, session['username'], session_id, session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
		#new_session = Session(session_id, session_topic, session_location, session_time, session_duration, session_capacity, session_fee)

		#new_seminar.add_seminar_session(new_session)
		#system.add_event(new_seminar)
			if session['staff']:
				staff = user_manager.get_user_by_name(session['username'])
				staff.add_new_post(new_seminar)
		#seminars.append(new_seminar)
		#print(system.get_events())
			flash('You added an event to EMS', 'success')
			return redirect(url_for('add_seminar'))
		except AddEventError as ave:
			return render_template('add_seminar.html',form=form, errors=ave.errors)
	return render_template('add_seminar.html',form=form)


@app.route('/edit_seminar/<seminar_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_seminar(seminar_id):
	edit_seminar = system.get_event_by_ids(seminar_id)
	form = EditSeminarForm(request.form, convenor=edit_seminar.convenor,event_name=edit_seminar.event_name,
						seminar_name=edit_seminar.seminar_name,
						event_info=edit_seminar.info)
	if request.method == 'POST': #nd form.validate():
		#Edit Seminar
		try:
			convenor = form.convenor.data
			event_name = form.event_name.data
			seminar_name = form.event_name.data
			event_info = form.event_info.data

			errors = check_add_seminar_error(convenor, event_name, event_info, seminar_name)
			if errors != {}:
				raise AddEventError(errors)
			edit_seminar.set_convenor(form.convenor.data)
			edit_seminar.set_event_name(form.event_name.data)
			edit_seminar.set_seminar_name(form.seminar_name.data)
			edit_seminar.set_info(form.event_info.data)
			#Edit Session
			#edit_event.set_location(form.session_location.data)
			#edit_event.set_duration(form.session_duration.data)
			#edit_event.set_time(form.session_time.data)
			#edit_event.set_capacity(form.session_capacity.data)
			flash('You edited a seminar on EMS', 'success')
			return redirect(url_for('home'))
		except AddEventError as ave:
			return render_template('edit_seminar.html',form=form, event=edit_seminar, errors=ave.errors)
	return render_template('edit_seminar.html',form=form, event=edit_seminar)


@app.route('/add_session/<seminar_id>', methods=['GET', 'POST'])
@is_logged_in
def add_session(seminar_id):
	#print("seminar_id: ", seminar_id)
	date_format = "%Y-%m-%d"
	seminar = system.get_event_by_ids(seminar_id)
	form = AddSessionForm(request.form)


	if request.method == 'POST': #nd form.validate():
		session_topic = form.session_topic.data
		session_location = form.session_location.data

		#session_time = request.form['session_time']
		#session_time = datetime.strptime(form.session_time.data, date_format)
		session_time = form.session_time.data
		print(session_time)
		print("SESSION TIME: ", session_time, type(session_time))
		early_bird = form.early_bird.data
		session_capacity = form.session_capacity.data
		session_fee = form.session_fee.data
		session_duration = form.session_duration.data

		session_id = system.ID_generator()
		try:
			system.add_extra_session(seminar, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		#new_session = Session(session_id, session_topic, session_location, session_time, session_duration, session_capacity)
		#seminar.add_seminar_session(new_session)

			flash('You added a session to EMS', 'success')
			return redirect(url_for('view_sessions', seminar_id=seminar_id, seminar=seminar))
		except AddEventError as ave:
			print("DIDIDID")
			return render_template('add_session.html',form=form, seminar_id=seminar_id, seminar=seminar, errors=ave.errors)
	return render_template('add_session.html', form=form, seminar_id=seminar_id, seminar=seminar)

@app.route('/edit_session/<seminar_id>/<session_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_session(seminar_id,session_id):
	print("seminar_id: ", seminar_id)
	seminar = system.get_event_by_ids(seminar_id)
	edit_session = seminar.get_session_by_ids(session_id)
	form = AddSessionForm(request.form, session_topic=edit_session.topic,
						session_location=edit_session.location,
						session_time=edit_session.time,
						session_capacity=edit_session.capacity,
						session_fee=edit_session.fee,
						session_duration=edit_session.duration)
	if request.method == 'POST': #nd form.validate():
		try:
			session_topic = form.session_topic.data
			session_location = form.session_location.data

			#session_time = request.form['session_time']
			#session_time = datetime.strptime(form.session_time.data, date_format)
			session_time = form.session_time.data
			early_bird = form.early_bird.data
			session_capacity = form.session_capacity.data
			session_fee = form.session_fee.data
			session_duration = form.session_duration.data
			errors = check_add_session_error(session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
			if errors != {}:
				raise AddEventError(errors)
			
			edit_session.set_topic(form.session_topic.data)
			edit_session.set_location(form.session_location.data)
			edit_session.set_time(form.session_time.data)
			edit_session.set_capacity(form.session_capacity.data)
			edit_session.set_fee(form.session_fee.data)
			edit_session.set_early_bird(form.early_bird.data)
			edit_session.set_duration(form.session_duration.data)

			flash('You edited a session on EMS', 'success')
			return redirect(url_for('view_sessions', seminar_id=seminar_id, seminar=seminar))
		except AddEventError as ave:
			return render_template('edit_session.html',form=form, seminar_id=seminar_id, seminar=seminar, errors=ave.errors)
	return render_template('edit_session.html', form=form, seminar_id=seminar_id, seminar=seminar, session_id=session_id, session = edit_session)


@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')

#display event information
@app.route('/event/<event_name>')
@is_logged_in
def event(event_name):
	event_info = system.get_info_by_name(event_name)
	return render_template('event.html', event_info=event_info)


@app.route('/home', methods=['GET', 'POST'])
@is_logged_in
def home():
	date_format = "%Y-%m-%d"
	Events = system.events
	courses = []
	seminars = []
	isStaff=session['staff']
	for event in Events:
		if event.__class__.__name__ == 'Course':
			if (datetime.strptime(event.time, date_format) - datetime.today()).days < 0:
				event.set_status("Closed")
			print(event._convenor)
			courses.append(event)
		elif event.__class__.__name__ == 'Seminar':
			seminars.append(event)
	#print(system.get_events())
	poster = session['username']
	return render_template('home.html', isStaff = session['staff'], isGuest = session['guest'], courses=courses, seminars=seminars, poster = poster)


# Dashboard display registered events for all users -- event posts for staffs
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
	current_user = session['username']
	current_user = user_manager.get_user_by_name(current_user)
	registered_events = current_user.get_registered_events()

	if session['staff']:
		staff = user_manager.get_user_by_name(session['username'])
		created_events = staff.get_created_events()
		return render_template('dashboard.html', reg_events=registered_events, isStaff = session['staff'], created_events=created_events)

	return render_template('dashboard.html', reg_events=registered_events, isStaff = session['staff'])


# user click to register to an event
@app.route('/register/<event_name>', methods=['GET', 'POST'])
@is_logged_in
def register(event_name):
	#print("USERS:", session['username'])
	#print(event_name)
	#print(system.get_events())
	date_format = "%Y-%m-%d"
	current_user = user_manager.get_user_by_name(session['username'])
	print("name: ", event_name)
	system.events
	event = system.get_event_by_name(event_name)
	print(event)

	if event.__class__.__name__ == 'Course':
		if (event.status == "Open"):
			check = system.add_course_trainee(event, current_user)

			if not check:
				flash('You already registered in this course before or check capacity', 'danger')
			else:
				print(event.early_bird)
				if (datetime.strptime(event.early_bird, date_format) - datetime.today()).days >= 0 and session['guest']:
					text = "Congratz Mate! Early bird - Get Half Price " + str((event.fee)/2)
					flash( text, 'success')

				user_manager.add_event_in_user(current_user, event)
				flash('Register successful', 'success')
		else:
			flash('The event was canceled', 'danger')

	### This is added straight away to Session not via Seminar #####
	### In this case event_name is session_topic ###
	else:
		seminar = None
		sessions = None
		sess = system.get_session_by_topic(event_name)
		if (sess.status == "Open"):
			for event in system.events:
				if event.__class__.__name__ == 'Seminar':
					for s in event.sessions_list:
						if s.topic == event_name:
							seminar = event
							sessions = event.sessions_list
							break

			check = system.add_session_trainee(event_name, current_user)
			if not check:
				flash('You already registered in this session before or check capacity', 'danger')
			else:
				if (datetime.strptime(sess.early_bird, date_format) - datetime.today()).days >= 0 and session['guest']:
					text = "Congratz Mate! Early bird - Get Half Price " + str((sess.fee)/2)
					flash(text, 'success')
				user_manager.add_event_in_user(current_user, sess)
				flash('Register successful', 'success')
			#print(sess._trainees)
			seminar = system.get_seminar_by_session_topic(event_name)
			poster = session['username']
			return render_template('session.html', isStaff = session['staff'], sessions=sessions, seminar=event, poster=poster)
		else:
			flash('The event was canceled', 'danger')
	return redirect(url_for('home'))


@app.route('/deregister/<event_name>', methods=['GET', 'POST'])
@is_logged_in
def deregister(event_name):
	print(system.events)
	current_user = user_manager.get_user_by_name(session['username'])
	event = system.get_event_by_name(event_name)
	print(event.__class__.__name__)

	if event.__class__.__name__ == 'Course':
		if(event._status == "Open"):
			check = system.remove_course_trainee(event, current_user)
			if not check:
				flash('You are not in this event', 'danger')
			else:
				user_manager.remove_event_in_user(current_user, event)
				flash('De-Register Successful - Thank you', 'success')
		else:
			flash('The event was canceled', 'danger')
	### This is added straight away to Session not via Seminar #####
	### In this case event_name is session_topic ###
	else:
		seminar = None
		sessions = None
		sess = system.get_session_by_topic(event_name)
		if(sess.status == "Open"):
			for event in system.events:
				if event.__class__.__name__ == 'Seminar':
					for s in event.sessions_list:
						if s.topic == event_name:
							seminar = event
							sessions = event.sessions_list
							break

			check = system.remove_session_trainee(event_name, current_user)
			if not check:
				flash('You are not in this session', 'danger')
			else:
				user_manager.remove_event_in_user(current_user, sess)
				flash('De-Register Successful - Thank you', 'success')
			seminar = system.get_seminar_by_session_topic(event_name)
			poster = session['username']
			#print(sess._trainees)
			return render_template('session.html', isStaff = session['staff'], sessions=sessions, seminar=event, poster=poster)
		else:
			flash('The event was canceled', 'danger')
	return redirect(url_for('home'))

@app.route('/cancel/<event_name>', methods=['GET', 'POST'])
@is_logged_in
def cancel(event_name):
	print(system.events)
	current_user = user_manager.get_user_by_name(session['username'])
	event = system.get_event_by_name(event_name)
	print(event.__class__.__name__)
	if event.__class__.__name__ == 'Course':
		event.set_status("Canceled");
		flash('The Course was canceled successfully', 'danger')
	if event.__class__.__name__ == 'Seminar':
		event.set_status("Canceled");
		for s in event.sessions_list:
			s.set_status("Canceled")
		flash('The Seminar was canceled successfully', 'danger')
	return redirect(url_for('home'))

@app.route('/open/<event_name>', methods=['GET', 'POST'])
@is_logged_in
def open(event_name):
	print(system.events)
	current_user = user_manager.get_user_by_name(session['username'])
	event = system.get_event_by_name(event_name)
	print(event.__class__.__name__)
	if event.__class__.__name__ == 'Course':
		event.set_status("Open");
		flash('The Course was reopened successfully', 'success')
	if event.__class__.__name__ == 'Seminar':
		event.set_status("Open");
		for s in event.sessions_list:
			s.set_status("Open")
		flash('The Seminar was reopened successfully', 'success')
	return redirect(url_for('home'))

@app.route('/cancel_session/<seminar_id>/<session_id>', methods=['GET', 'POST'])
@is_logged_in
def cancel_session(seminar_id,session_id):
	print("seminar_id: ", seminar_id)
	seminar = system.get_event_by_ids(seminar_id)
	edit_session = seminar.get_session_by_ids(session_id)
	edit_session.set_status("Canceled")
	return redirect(url_for('view_sessions', seminar_id=seminar_id, seminar=seminar))

@app.route('/open_session/<seminar_id>/<session_id>', methods=['GET', 'POST'])
@is_logged_in
def open_session(seminar_id,session_id):
	print("seminar_id: ", seminar_id)
	seminar = system.get_event_by_ids(seminar_id)
	edit_session = seminar.get_session_by_ids(session_id)
	edit_session.set_status("Open")
	return redirect(url_for('view_sessions', seminar_id=seminar_id, seminar=seminar))

@app.route('/viewsessions/<seminar_id>', methods=['GET', 'POST'])
@is_logged_in
def view_sessions(seminar_id):
	date_format = "%Y-%m-%d"
	print("EVENT NAME: ", seminar_id)
	seminar = system.get_event_by_ids(seminar_id)
	print("SEMINAR: ", seminar)
	sessions = seminar.sessions_list
	for s in sessions:
		if (datetime.strptime(s.time, date_format) - datetime.today()).days < 0:
			s.set_status("Closed")
		print(s.topic)

	poster = session['username']
	return render_template('session.html', isStaff = session['staff'], sessions=sessions, seminar=seminar, poster=poster)
