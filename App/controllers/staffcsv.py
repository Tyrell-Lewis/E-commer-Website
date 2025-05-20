import csv
import secrets
import string
from flask import current_app
from flask_mailman import EmailMultiAlternatives
from App.models import *
from App.controllers.staff import create_staff
from App.database import db


def generate_random_password(length=12):
  alphabet = string.ascii_letters + string.digits + string.punctuation
  return ''.join(secrets.choice(alphabet) for _ in range(length))


def populate_staff_from_csv(csv_file_path):
  try:
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        firstname = row.get('First name')
        lastname = row.get('Last name')
        username = f"{firstname}.{lastname}" if firstname and lastname else ""
       
        email = row.get('Email address')

        if None in [firstname, lastname, username,email]:
          print("Some values in the row are None.")
          continue

        # Generate a random, secure password for each student
        password = generate_random_password()

        new_staff = create_staff(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,  # Use the generated password
            faculty="",
        )

        if new_staff:
          print(f"User created: {firstname} {lastname}")
          # Prepare and send the email with the new account details
          subject = "Welcome to Our Student Conduct Tracker Platform!"
          body = f"Dear {firstname},\n\nYour new Staff account has been created.\n\nUsername: {username}\nPassword: {password}\n\nPlease ensure you change your password upon first login."

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
