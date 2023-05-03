# from django.db import models
from pprint import pprint
from Google import Create_Service, convert_to_RFC_datetime
# from doctor.models import Appointment
# from hospital.models import
import os

def make_event(app_date, app_time):
    print("-------------------------------------------------------")
    print("app_date = ",app_date)
    print("app_time = ",app_time)
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,SCOPES)

    request_body = {
            'summary' : 'Mentcare'
    }
    page_token = None
    calendar_exists = False
    calender_id = ''
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        #loops through the list of all calendars
        for calendar_list_entry in calendar_list['items']:
            pprint(calendar_list_entry['summary'])
            # if we find the calendar exists, then we skip making it, and go straight to creating event
            if 'Mentcare' == calendar_list_entry['summary']:
                calendar_exists = True
                calender_id = calendar_list_entry['id']
                print("The calender id: ",calender_id)
                pprint('mentcare is already in here man!!!')
                break
        if calendar_exists == False:
            pprint("The calendar DOESNT exist")
            response = service.calendars().insert(body=request_body).execute()
            calender_id = response['id']
            pprint("The calender id: ",calender_id)
        # create an event using the date froma doctor model appointment 
        hour_adjustment = 4 # adjustment for New York timezone
        months = {
                'January':1,
                'February':2,
                'March':3,
                'April':4,
                'May':5,
                'June':6,
                'July':7,
                'August':8,
                'September':9,
                'October':10,
                'November':11,
                'December':12
                }
        str(app_date)
        str(app_time)
        date_of_appointment = app_date.split() #index vals - 0:Month 1:Day w/ a comma 2: Year
        date_of_appointment[0] = months[ str(date_of_appointment[0]) ]
        date_of_appointment[1] = date_of_appointment[1][:len(date_of_appointment[1])-1]
        time_of_appointment = app_time.split(':') #expected to see ex. "6:12", so ind 0 is 6 and ind 1 is 12

        for i in range(len(date_of_appointment)):
            date_of_appointment[i] = int(date_of_appointment[i])
        for i in range(len(time_of_appointment)):
            time_of_appointment[i] = int(time_of_appointment[i])
        # event_request_body = {
        #     'start' : {
        #         'dateTime': convert_to_RFC_datetime(2023, 8, 1, 12 + hour_adjustment, 30),
        #         'timeZone':'America/New_York'
        #         },
        #     'end' : {
        #         'dateTime': convert_to_RFC_datetime(2023, 8, 1, 12 + hour_adjustment + 1, 00),
        #         'timeZone':'America/New_York'
        #         },
        #     'summary': 'Mentcare Doctor Appointment',
        #     'description': 'Coming into NJIT hospital for a psychiatrist visit.',
        #     'colorId': 3,
        #     'status': 'confirmed',
        #     'transparency': 'opaque',
        #     'visibility': 'private',
        #     'location': 'Newark, NJ',
        # } 
        event_request_body = {
            'start' : {
                'dateTime': convert_to_RFC_datetime(date_of_appointment[2], 
                                                    date_of_appointment[0], 
                                                    date_of_appointment[1], 
                                                    time_of_appointment[0]+ hour_adjustment, 
                                                    time_of_appointment[1]),
                'timeZone':'America/New_York'
                },
            'end' : {
                #added 45 to time so the appointment lasts 45 minutes

                'dateTime': convert_to_RFC_datetime(date_of_appointment[2], 
                                                    date_of_appointment[0], 
                                                    date_of_appointment[1], 
                                                    time_of_appointment[0] + hour_adjustment, 
                                                    time_of_appointment[1] + 45),
                'timeZone':'America/New_York'
                },
            'summary': 'Mentcare Doctor Appointment',
            'description': 'Coming into NJIT hospital for a psychiatrist visit.',
            'colorId': 3,
            'status': 'confirmed',
            'transparency': 'opaque',
            'visibility': 'private',
            'location': 'Newark, NJ',
        } 
        max_Attendees = 2
        send_notification = True
        sendUpdate = 'none'
        supports_attachments = False
        calender_id = str(calender_id)
        response = service.events().insert(
                calendarId=calender_id,
                maxAttendees=max_Attendees,
                sendNotifications=send_notification,
                sendUpdates=sendUpdate,
                supportsAttachments=supports_attachments,
                body=event_request_body,
                ).execute()
        pprint(response)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

if __name__ == "__main__":
    make_event("May 2, 2023", "6:12") # just a test



