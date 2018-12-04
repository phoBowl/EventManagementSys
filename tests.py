#from flask import url_for, session, request
from model.client import *
from model.EMS import *
from model.Errors import *
import pytest
from model.User_Manager import *
#  (1) create a seminar 
#  (2) register a guestuser
# into the EMS 
# (3) register for a seminar by student 
# (4) register for a seminar by guest-user
# (5) team to choose the fifth user-story

class TestingSeminar():
	def test_empty_seminar_name(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = ""
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-07-01"
		early_bird = "2018-06-01"
		session_duration = 6
		session_capacity = 8
		session_fee = 20
		check = None
		try:
			check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		# 	assert 1==0
			
		except AddEventError as ave:
			assert 'seminar name' in ave.msg
		#	assert 'seminar_name' in avg._msg
		assert check is None

	def test_empty_seminar_date(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = ""
		early_bird = "2018-06-01"
		session_duration = 6
		session_capacity = 8
		session_fee = 20
		check = None
		
		try:
			check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		# 	assert 1==0
			
		except AddEventError as ave:
			assert 'Invalid Date' in ave.msg
		assert check is None
	# """First Session day is already passed"""
	def test_seminar_date1(n):
		
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-05-20"
		early_bird = "2018-06-01"
		session_duration = 6
		session_capacity = 8
		session_fee = 20
		check = None
		try:
			check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		# 	assert 1==0
			
		except AddEventError as ave:
			assert 'Invalid Date' in ave.msg
		assert check is None
	# Duration is a string
	def test_seminar_date2(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-07-11"
		early_bird = "2018-06-01"
		session_duration = "STRING"
		session_capacity = 8
		session_fee = 20

		check = None
		try:
			check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		# 	assert 1==0
			
		except AddEventError as ave:
			assert 'duration' in ave.msg
		assert check is None
	## Test capacity is string
	def test_seminar_date3(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-07-11"
		early_bird = "2018-06-01"
		session_duration = 6
		session_capacity = "STRING"
		session_fee = 20
		check = None
		errors = check_add_session_error(session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
		
		try:
			
			check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
			
		
		except AddEventError as ave:
			assert 'capacity' in ave.msg
		assert check is None
	##fee, capacity, duration is string
	def test_seminar_date4(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-07-11"
		early_bird = "2018-06-01"
		session_duration = "STRING"
		session_capacity = "STRING"
		session_fee = "STRING"
		check = None
		errors = check_add_session_error(session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
		try:
			check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		# 	assert 1==0
		except AddEventError as ave:
			assert 'duration' in ave.msg
			assert 'fee' in ave.msg
			assert 'capacity' in ave.msg
		assert check is  None

	## Non Staff create seminar
	def test_student_seminar(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-07-11"
		early_bird = "2018-06-01"
		session_duration = "STRING"
		session_capacity = "STRING"
		session_fee = "STRING"
		check = None
		try:
			check = system.add_seminar(False,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		# 	assert 1==0
			
		except AddEventError as ave:
			assert 'duration' in ave.msg
			assert 'fee' in ave.msg
			assert 'capacity' in ave.msg
		assert check is  None

	# success case
	def test_staff_seminar(n):
		system = ems_system()
		user_manager = user_manager_system()
		seminar_id = system.ID_generator()
		convenor = "HIEU"
		event_name = "sddd"
		event_info = "dqwd"
		seminar_name = "Cooking"
		user = "name4119992"
		session_id = system.ID_generator()
		session_topic = "dwed"
		session_location = "dqwed"
		session_time = "2018-07-11"
		early_bird = "2018-06-01"
		session_duration = 6
		session_capacity = 8
		session_fee = 9
		check = None
		check = system.add_seminar(True,seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee)
		assert check is not None

class TestingGuestRegister():
	def test_register(m):
		''' Emtpy all the field '''
		system = ems_system()
		user_manager = user_manager_system()
		check = None
		zID = None
		name = ""
		email = ""
		password = ""
		try:
			check = user_manager.add_user(zID,name,email,password)
		except RegisterError as re:
			assert 'name' in re.msg
			assert 'email' in re.msg
			assert 'password' in re.msg
		assert check is None
	
	def test_register1(m):
		''' Emtpy  name '''
		system = ems_system()
		user_manager = user_manager_system()
		check = None
		zID = None
		name = ""
		email = "hieumai@gmail.com"
		password = "123"
		try:
			check = user_manager.add_user(zID,name,email,password)
		except RegisterError as re:
			assert 'name' in re.msg
			assert 'email' not in re.msg
			assert 'password' not in re.msg
		assert check is None