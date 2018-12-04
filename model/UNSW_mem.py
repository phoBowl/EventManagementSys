from abc import ABC
from flask_login import UserMixin

class User(UserMixin, ABC):
	__id = -1
	def __init__(self, email, password):
		self._id = self._generate_id()
		self._email = email
		self._password = password
		self._eventRegister = []

	@property
	def email(self):
		return self._email

	@property
	def get_course_Register(self):
		return self._eventRegister

	def add_register_event(self, event):
		self._eventRegister.append(event)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	def get_id(self):
		"""Required by Flask-login"""
		return str(self._id)

	def _generate_id(self):
		User.__id += 1
		return User.__id

	def validate_password(self, password):
		return self._password == password

class Student(User):
	def __init__(self, zID, password, name, email):
		super().__init__(email, password)
		self._name = name
		self._email = email
		self._registered_events = []

	#def __str__(self):
	#	return "Student Details: name - {}, zID - {}, email - {}".format(self._name, self._zID, self._email)
	@property
	def name(self):
		return str(self._name)

	@property
	def email(self):
		return str(self._email)

	def is_Staff(self):
		return False

	def is_Guest(self):
		return False

	def add_event(self, event):
		self._registered_events.append(event)

	def remove_event(self, event):
		self._registered_events.remove(event)

	def get_registered_events(self):
		return self._registered_events

class Staff(User):
	def __init__(self, zID, password, name, email):
		super().__init__(email, password)
		self._name = name
		self._email = email
		self._registered_events = []
		self._created_events = []
	#def __str__(self):
	#	return "Staff Details: name - {}, zID - {}, email - {}".format(self._name, self._zID, self._email)
	@property
	def name(self):
		return str(self._name)

	@property
	def email(self):
		return str(self._email)

	def is_Staff(self):
		return True

	def is_Guest(self):
		return False

	def add_event(self, event):
		self._registered_events.append(event)

	def remove_event(self, event):
		self._registered_events.remove(event)

	def add_new_post(self, event):
		self._created_events.append(event)

	def cancel_post(self, event):
		self._created_events.remove(event)

	def get_registered_events(self):
		return self._registered_events

	def get_created_events(self):
		return self._created_events

class Guest(User):
	#zID and is None in this case - Guest dont have zID
	def __init__(self, zID, name, email, password):
		super().__init__(zID, password)
		self._name = name
		self._email = email
		self._registered_events = []

	#def __str__(self):
	#	return "Student Details: name - {}, zID - {}, email - {}".format(self._name, self._zID, self._email)
	@property
	def name(self):
		return str(self._name)

	def is_Staff(self):
		return False

	def is_Guest(self):
		return True

	def add_event(self, event):
		self._registered_events.append(event)

	def remove_event(self, event):
		self._registered_events.remove(event)

	def get_registered_events(self):
		return self._registered_events