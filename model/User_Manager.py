from model.UNSW_mem import User, Student, Staff, Guest
from model.Errors import *

class User_Manager:
	def __init__(self):
		self._UNSWmems = []

	@property
	def UNSWmems():
		return self._UNSWmems

	def add_user(self, zID, name, email, password):
		user = Guest(zID, name,email,password)
		errors = check_register_error(name, email, password)
		if errors != {}:
			raise RegisterError(errors)
		else:
			if user not in self._UNSWmems and not self.isEmailExist(user.email):
				self._UNSWmems.append(user)
				return True
			else:
				return False

	def isEmailExist(self, email):
		for mem in self._UNSWmems:
			if mem.email == email:
				print("YES EXIST")
				return True
		return False

	def get_user_by_name(self,name):
		for mem in self._UNSWmems:
			if mem.name == name:
				return mem

	def validate_login(self, email, password):
		for mem in self._UNSWmems:
			if mem.email == email and mem.validate_password(password):
				return mem
		return None

	def get_user_by_id(self, user_id):
		for c in self._UNSWmems:
			if c.get_id() == user_id:
				return c
		return None

	# whenever a user register an event, they themselves add that event to their list
	def add_event_in_user(self, user, event):
		for u in self._UNSWmems:
			if user.name == u.name:
				user.add_event(event)

	def remove_event_in_user(self, user, event):
		for u in self._UNSWmems:
			if user.name == u.name:
				user.remove_event(event)