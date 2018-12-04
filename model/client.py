import csv
import datetime
from .EMS import EMS
from .UNSW_mem import User, Student, Staff
from .Event import Course, Seminar, Session
from .User_Manager import User_Manager

def user_manager_system():
	user_manager = User_Manager()
	users = list() #list of unsw members
	with open('user.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['role'] == 'trainee':
				users.append(Student(row['zID'],row['password'],row['name'],row['email']))
			elif row['role'] == 'trainer':
				users.append(Staff(row['zID'],row['password'],row['name'],row['email']))
			
	user_manager._UNSWmems = users
	return user_manager

def ems_system():
	system = EMS()
	events = list() #list of events
	
	event1 = Course(1,'John', 'MATHH', 'OKOK do math', 'MATH1A', 'UNSW K17', '2018-05-05','2018-03-03' ,2, 'name4119990', 0, 70)
	event2 = Course(2,'Ronan', 'Food', 'OKOK eat', 'FOOD1239', 'UNSW Food court', '2018-05-05', '2018-03-03',2, 'name4119989', 50, 30)

	seminar1 = Seminar(3,'Hieu', 'Cooking festival', 'Teach you cook? Ok ' ,'How to cook quick', 'name4119992')
	session1 = Session(3,'Cook-episode 1', 'UNSW Kitchen', '2018-05-05', '2018-03-03', 5, 30, 70)

	seminar1.add_seminar_session(session1)

	system.add_event(event1)
	system.add_event(event2)
	system.add_event(seminar1)
	return system
