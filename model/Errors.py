from datetime import datetime, timedelta

class AddEventError(Exception):

    def __init__(self, errors, msg=None):
        if msg is None:
            self.msg = "error occurs with fields: %s"%(', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors

class RegisterError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            self.msg = "error occurs with fields: %s"%(', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors

def check_register_error(name,email,password):
    errors = {}
    if name == '':
        errors['name'] = "Please Do Not Leave Name Empty"

    if email == '':
        errors['email'] = "Please Do Not Leave Email Empty"

    if password == '':
        errors['password'] = "Please Do Not Leave Password Empty"


    return errors

def check_add_course_error(date_time, early_bird, convenor, event, course_name, location, duration, capacity,fee):
    errors = {}
    date_format = "%Y-%m-%d"

    try:
        datetime.strptime(date_time, date_format)
    except:
        errors['Invalid Date'] = "Please Do Not Leave Your Date Empty or Make sure date is in YYYY-MM-DD format"
    
    try:
        datetime.strptime(early_bird, date_format)
    except:
        errors['Invalid Early Bird'] = "Early Bird is Empty or Make sure date is in YYYY-MM-DD format"

    if convenor == '':
        errors['Convenor'] = "Specify a valid Convenor"

    if event == '':
        errors['event'] = "Dont leave Event Name Empty"

    if course_name == '':
        errors['course name'] = "Dont leave course name Empty"

    if location == '':
        errors['location'] = "Dont leave location Empty"

    try:
        float(duration)
    except:
        errors['duration'] = "Please Enter Valid Duration"

    try:
        int(capacity)
        #    errors['capacity'] = "Please Input valid capacity"
    except:
        errors['capacity'] = "Please Input valid capacity"

    try:
        float(fee)
    except:
        errors['fee'] = "Please Input valid Fee for Guest"



    # if end_location == '':
    #     errors['end_location'] = "Specify a valid end location"



    if 'Invalid Date' not in errors:

        if (datetime.strptime(date_time, date_format) - datetime.today()).days <= 0:
            errors['Invalid Date'] = "Please Input A valid Date - also at least one day before the course start"

    if 'Invalid Early Bird' not in errors and 'Invalid Date' not in errors:
        if (datetime.strptime(date_time, date_format) - datetime.strptime(early_bird,date_format)).days <= 0:
            errors['Invalid Early Bird'] = "Early Bird Period Must before the start date"
        
    return errors


def check_add_seminar_error(convenor, event_name, event_info, seminar_name):
    errors = {}

    if convenor == '':
        errors['Convenor'] = "Specify a valid Convenor"

    if event_name == '':
        errors['event'] = "Dont leave Event Name Empty"

    if event_info == '':
        errors['even info'] = "Dont leave event info Empty"

    if seminar_name == '':
        errors['seminar name'] = "Dont leave seminar name empty"

    return errors


def check_add_session_error(session_topic, session_location, session_time, early_bird, session_duration, session_capacity, session_fee):
    errors = {}
    date_format = "%Y-%m-%d"

    try:
        datetime.strptime(session_time, date_format)
    except:
        errors['Invalid Date'] = "Please Do Not Leave Your Date Empty or Make sure date is in YYYY-MM-DD format"

    try:
        datetime.strptime(early_bird, date_format)
    except:
        errors['Invalid Early Bird'] = "Early Bird is Empty  or Make sure date is in YYYY-MM-DD format"
    
    if session_topic == '':
        errors['topic'] = "Specify a valid topic"


    if session_location == '':
        errors['location'] = "Dont leave location Empty"

    try:
        float(session_duration)
    except:
        errors['duration'] = "Please Enter Valid Duration"

    try:
        int(session_capacity)
        #    errors['capacity'] = "Please Input valid capacity"
    except:
        errors['capacity'] = "Please Input valid capacity"

    try:
        float(session_fee)
    except:
        errors['fee'] = "Please Input valid session Fee for Guest"


    # if end_location == '':
    #     errors['end_location'] = "Specify a valid end location"

    if 'Invalid Date' not in errors:
        if (datetime.strptime(session_time, date_format) - datetime.today()).days <= 0:
            errors['Invalid Date'] = "Please Input A valid Date - also at least one day before the course start"

    if 'Invalid Early Bird' not in errors and 'Invalid Date' not in errors:
        if (datetime.strptime(session_time, date_format) - datetime.strptime(early_bird,date_format)).days <= 0:
            errors['Invalid Early Bird'] = "Early Bird Period Must before the start date"

    return errors

#class RegisterError():
