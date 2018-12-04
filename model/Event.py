from abc import ABC

class Event(ABC):
	def __init__(self, ids, convenor, event_name, info, poster):
		self._ids = ids
		self._convenor = convenor #string
		self._event_name = event_name #string
		self._info = info #string
		self._poster = poster

	@property
	def ids(self):
		return self._ids

	@property
	def convenor(self):
		return self._convenor

	@property
	def event_name(self):
		return self._event_name

	@property
	def info(self):
		return self._info

	@property
	def poster(self):
		return self._poster

	def set_convenor(self,convenor):
		self._convenor = convenor

	def set_event_name(self,event_name):
		self._event_name = event_name

	def set_info(self,info):
		self._info = info

class Course(Event):

	def __init__(self, ids, convenor, event_name, info, course_name, location, time, early_bird, duration, poster, capacity, fee, status= "Open"):
		super().__init__(ids, convenor, event_name, info, poster)
		self._course_name = course_name #string
		self._location = location #string
		self._time = time #datetime
		self._early_bird = early_bird #datetime
		self._duration = duration #float
		self._capacity = capacity #int
		self._trainees = []
		self._fee = fee
		self._status = status

	# @property
	# def get_id(self):
	# 	return self._id

	@property
	def course_name(self):
		return self._course_name

	@property
	def location(self):
		return self._location

	@property
	def time(self):
		return self._time

	@property
	def early_bird(self):
		return self._early_bird

	@property
	def duration(self):
		return self._duration

	@property
	def capacity(self):
		return self._capacity

	@property
	def fee(self):
		return self._fee

	@property
	def status(self):
		return self._status

	def set_course_name(self,course_name):
		self._course_name = course_name

	def set_location(self,location):
		self._location = location

	def set_time(self,time):
		self._time = time

	def set_duration(self,duration):
		self._duration = duration

	def set_capacity(self, capacity):
		self._capacity = capacity

	def set_fee(self, fee):
		self._fee = fee

	def set_early_bird(self, early_bird):
		self._early_bird = early_bird

	def set_status(self, status):
		self._status = status

	def number_of_trainees(self):
		counter = 0
		for t in self._trainees:
			counter = counter + 1
		return counter

	def add_trainee(self,trainee):
		if trainee in self._trainees:
			return False

		if self.number_of_trainees() < int(self.capacity):
			#TRY CATCH HERE 3
			self._trainees.append(trainee)
			return True

	def remove_trainee(self,trainee):
		if trainee not in self._trainees:
			return False
		self._trainees.remove(trainee)
		return True

	def get_trainees(self):
		return self._trainees


class Seminar(Event):
	"""docstring for Seminar"""
	def __init__(self, ids, convenor, event_name, info, seminar_name, poster, status="Open"):
		super().__init__(ids, convenor, event_name,info, poster)
		self._seminar_name = seminar_name #string
		self._sessions = [] #list
		self._status = status
	# getter methods
	# @property
	# def get_id(self):
	# 	return self._id

	@property
	def seminar_name(self):
		return self._seminar_name

	@property
	def sessions_list(self):
		return self._sessions

	@property
	def status(self):
		return self._status

	# setter methods
	def set_seminar_name(self, name):
		self._seminar_name = name
		return None

	def add_seminar_session(self, session):
		self._sessions.append(session)
		return None

	def set_status(self, status):
		self._status = status

	def remove_seminar_session(self, session):
		if session in self._sessions:
			self._sessions.remove(session)
			return True
		return False

	def get_session_by_ids(self, session_id):
		for s in self._sessions:
			if int(s.ids) == int(session_id):
				return s

class Session():
	def __init__(self, ids, topic, location, time, early_bird, duration, capacity, fee, status = "Open"):
		#super().__init__(seminar_name)
		self._ids = ids
		self._topic = topic #string
		self._location = location #string
		self._time = time #datetime
		self._early_bird = early_bird
		self._duration = duration #float
		self._capacity = capacity
		self._trainees = [] #list
		self._fee = fee
		self._status = status
	# getter methods
	@property
	def ids(self):
		return self._ids

	@property
	def topic(self):
		return self._topic

	@property
	def location(self):
		return self._location

	@property
	def time(self):
		return self._time

	@property
	def early_bird(self):
		return self._early_bird

	@property
	def duration(self):
		return self._duration

	@property
	def capacity(self):
		return self._capacity

	@property
	def fee(self):
		return self._fee

	@property
	def status(self):
		return self._status

	@property
	def trainees(self):
		return self._trainees

	def number_of_trainees(self):
		counter = 0
		for t in self._trainees:
			counter = counter + 1
		return counter

	# setter methods
	def set_topic(self, topic_name):
		self._topic = topic_name
		return None

	def set_location(self, location_name):
		self._location = location_name
		return None

	def set_time(self, date_time):
		self._time = date_time
		return None

	def set_duration(self, length):
		self._duration = length
		return None

	def set_capacity(self, capacity):
		self._capacity = capacity

	def set_fee(self, fee):
		self._fee = fee

	def set_early_bird(self, early_bird):
		self._early_bird = early_bird
		
	def set_status(self, status):
		self._status = status
		
	def add_trainee(self, trainee): #boolean return
		if trainee in self._trainees:
			return False
			#TRY CATCH HERE 3
		if self.number_of_trainees() < int(self.capacity):
			self._trainees.append(trainee)
			return True

	def remove_trainee(self, trainee): #boolean return
		if trainee in self._trainees:
			self._trainees.remove(trainee)
			return True
		return False
