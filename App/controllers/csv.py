import csv
import secrets
import string
from flask import current_app
from flask_mailman import EmailMultiAlternatives
from App.models import *
from App.controllers.student import create_student, get_student_by_UniId
from App.controllers.karma import  create_karma, get_karma
from App.database import db  


def generate_random_password(length=12):
  alphabet = string.ascii_letters + string.digits + string.punctuation
  return ''.join(secrets.choice(alphabet) for _ in range(length))


def populate_db_from_csv(csv_file_path):
  try:
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        firstname = row.get('First name')
        lastname = row.get('Last name')
        username = f"{firstname}.{lastname}" if firstname and lastname else ""
        UniId = row.get('ID number')
        email = row.get('Email address')

        if None in [firstname, lastname, username, UniId, email]:
          print("Some values in the row are None.")
          continue

        # Generate a random, secure password for each student
        password = generate_random_password()

        #check if student exists in db
        student = get_student_by_UniId(UniId)
        #if not student:
        if student:
          print ('student already exist')
          return
        new_student = create_student(
            username=username,
            UniId=UniId,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,  # Use the generated password
            faculty="",
            admittedTerm="",
            degree="",
            gpa="",
        )

        if new_student:
          print(f"User created: {firstname} {lastname}")
          # Prepare and send the email with the new account details
          subject = "Welcome to Our Student Conduct Tracker Platform!"
          body = f"Dear {firstname},\n\nYour new Student account has been created.\n\nUsername: {username}\nPassword: {password}\n\nPlease ensure you change your password upon first login."
          
        #get student by new uniid
          student = get_student_by_UniId(UniId)
          if student:
            print(student.ID)
            create_karma(student.ID)
            student.karmaID = get_karma(student.ID).karmaID
            print(get_karma(student.ID).karmaID)
            db.session.commit()
            
          # Send email notification
          with current_app.app_context():
            email_message = EmailMultiAlternatives(subject=subject,
                                                   body=body,
                                                   to=[email])
            email_message.send()
        else:
          print(f"Failed to create user: {firstname} {lastname}")
  except Exception as e:
    print(f"An error occurred while processing the CSV file: {str(e)}")
