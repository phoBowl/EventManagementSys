import csv

##### THIS DOES NOTHING---- JUST A FUNCTION EXTRACT CSV file
######## HAVE A LOOK AT model/client.py
def csv_extract()
	system = EMS()
	
	users = list()
	with open('user.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			temp_user = {}
			temp_user['name'] = row['name']
			temp_user['zID'] = row['zID']
			temp_user['email'] = row['email']
			temp_user['password'] = row['password']
			temp_user['role'] = row['role']
			users.append(temp_user)
	return users
# for user in users:
# 	print(user)
