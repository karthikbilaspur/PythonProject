import os
import csv
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Google Classroom API settings
SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.coursework.students']

# Load CSV data
def load_csv_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Create Google Classroom API client
def create_client():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    return service

# Create course
def create_course(service, course_name, description):
    course = {
        'name': course_name,
        'description': description,
        'room': 'Online',
        'ownerId': 'me'
    }
    response = service.courses().create(body=course).execute()
    return response.get('id')

# List courses
def list_courses(service):
    response = service.courses().list().execute()
    courses = response.get('courses', [])
    return courses

# Create assignment
def create_assignment(service, course_id, title, description):
    assignment = {
        'title': title,
        'description': description,
        'state': 'PUBLISHED'
    }
    response = service.courses().courseWork().create(
        courseId=course_id, body=assignment).execute()
    return response.get('id')

# List assignments
def list_assignments(service, course_id):
    response = service.courses().courseWork().list(courseId=course_id).execute()
    assignments = response.get('courseWork', [])
    return assignments

# NLP functionality (basic)
def process_query(query):
    if query.lower() == 'what are my courses?':
        return list_courses(create_client())
    else:
        return 'Sorry, I didn\'t understand your query.'

# Main function
def main():
    service = create_client()
    csv_data = load_csv_data('courses.csv')

    while True:
        print('1. Create course')
        print('2. List courses')
        print('3. Create assignment')
        print('4. List assignments')
        print('5. Ask a question')
        choice = input('Enter your choice: ')

        if choice == '1':
            course_name = input('Enter course name: ')
            description = input('Enter course description: ')
            course_id = create_course(service, course_name, description)
            print(f'Course created with ID: {course_id}')
        elif choice == '2':
            courses = list_courses(service)
            for course in courses:
                print(course.get('name'))
        elif choice == '3':
            course_id = input('Enter course ID: ')
            title = input('Enter assignment title: ')
            description = input('Enter assignment description: ')
            assignment_id = create_assignment(service, course_id, title, description)
            print(f'Assignment created with ID: {assignment_id}')
        elif choice == '4':
            course_id = input('Enter course ID: ')
            assignments = list_assignments(service, course_id)
            for assignment in assignments:
                print(assignment.get('title'))
        elif choice == '5':
            query = input('Enter your query: ')
            response = process_query(query)
            print(response)

if __name__ == '__main__':
    main()