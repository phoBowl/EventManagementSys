from random import *
from model.Event import *
from model.Errors import *

class EMS:
	def __init__(self):
		#self._UNSWmems = []
		self._events = []

	def add_event(self, event):
		self._events.append(event)

	def add_course(self, coures_id, convenor, event, info, course_name, location, date_time, early_bird, duration, poster, capacity,fee):
		errors = check_add_course_error(date_time, early_bird, convenor, event, course_name, location, duration, capacity,fee)
		if errors != {}:
			raise AddEventError(errors)
		else:
			new_event = Course(coures_id, convenor, event, info, course_name, location, date_time, early_bird, duration, poster, capacity,fee )
			self.add_event(new_event)
			return new_event

	####### Only Apply for case Create New Seminar fix later #######
	def add_session(self,session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee):
		errors = check_add_session_error(session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
		if errors != {}:
			raise AddEventError(errors)
		else:
			new_session = Session(session_id, session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
			return new_session 

	def add_seminar(self, isStaff, seminar_id,convenor, event_name, event_info, seminar_name, user, session_id, session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee):
		print("dwefwe: ", isStaff)
		if isStaff:
			check = None
			new_session = self.add_session(session_id, session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
			errors = check_add_seminar_error(convenor, event_name, event_info, seminar_name)
			if errors != {}:
				print("1")
				print(errors)
				raise AddEventError(errors)
			else:
				new_seminar = Seminar(seminar_id,convenor, event_name, event_info, seminar_name, user)
				new_seminar.add_seminar_session(new_session)
				self.add_event(new_seminar)
				return new_seminar

	def add_extra_session(self, seminar, session_id, session_topic, session_location, session_time, early_bird,session_duration, session_capacity,session_fee):
		errors = check_add_session_error(session_topic, session_location, session_time, early_bird,session_duration, session_capacity,session_fee)
		if errors != {}:
			raise AddEventError(errors)
		else:
			new_session = Session(session_id, session_topic, session_location, session_time, early_bird,session_duration, session_capacity, session_fee)
			seminar.add_seminar_session(new_session)
			return new_session

	@property
	def events(self):
		for e in self._events:
			print(e.event_name)
		return self._events

	def get_event_by_ids(self, ids):
		for event in self._events:
			print("ID: ", ids , event.ids)
			if int(event.ids) == int(ids):
				print("Event: ", event)
				return event

	def get_info_by_name(self, event_name):
		for event in self._events:
			if event.event_name == event_name:
				return event.info

	def get_event_by_name(self, event_name):
		for event in self._events:
			if event.event_name == event_name:
				return event

	def get_session_by_topic(self,session_topic):
		for event in self._events:
		#	if event.get_event_name == event_name:
			if event.__class__.__name__ == 'Seminar':
				sessions = event.sessions_list
				for s in sessions:
					if s.topic == session_topic:
						return s

	def get_seminar_by_session_topic(self, session_topic):
		for event in self._events:
		#	if event.get_event_name == event_name:
			if event.__class__.__name__ == 'Seminar':
				sessions = event.sessions_list
				for s in sessions:
					if s.topic == session_topic:
						return event

	#add Trainee for COURSE event
	def add_course_trainee(self, event, trainee):
		event = self.get_event_by_name(event.event_name)
		check = event.add_trainee(trainee)
		if check:
			# ts  = event.get_trainees()
			# for t in ts:
			# 	print("name: ", t.get_name())
			#print(trainee.get_registered_events())
			return True
		else:
			print(trainee.get_registered_events())
			return False

	def remove_course_trainee(self, event, trainee):
		event = self.get_event_by_name(event.event_name)
		check = event.remove_trainee(trainee)
		if check:
			# self.remove_event_in_user(trainee, event)
			# ts  = event.get_trainees()
			# for t in ts:
			# 	print("name: ", t.get_name())
			# 	print(trainee.get_registered_events())
			return True
		else:
			print(trainee.get_registered_events())
			return False

	def add_session_trainee(self, session_topic, trainee):
		#event = self.get_event_by_name(event.get_event_name)
		for event in self._events:
			if event.__class__.__name__ == 'Seminar':
				for s in event.sessions_list:
					if s.topic == session_topic:
						check = s.add_trainee(trainee)
						if check:
							return True
						else:
							return False

	def remove_session_trainee(self, session_topic, trainee):
		for event in self._events:
			if event.__class__.__name__ == 'Seminar':
				for s in event.sessions_list:
					if s.topic == session_topic:
						check = s.remove_trainee(trainee)
						if check:
							return True
						else:
							return False

	# def check_early_bird(self, event_date, early_bird)

    # Get all ids of event in event list
	def get_ids(self):
		#print("A")
		id_list = []
		for event in self._events:
			id_list.append(event.ids)
		return id_list

	#randomly generate order ID
	def ID_generator(self):
	    randomID = randint(1,1000)
	    id_list = self.get_ids()
	    if randomID in id_list:
	        self.ID_generator()
	    else:
	        print(randomID)
	        return randomID
