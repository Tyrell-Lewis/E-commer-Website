import secrets
import string
import csv
from App.models import *
from App.controllers.user import create_user
from App.database import db

def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def populate_db_from_csv(csv_file_path):
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row.get('username')
                if not username:
                    # Generate a default username if it's missing
                    username = f"{row.get('firstname')}.{row.get('lastname')}"

                # Generate a random password
                password = generate_random_password()

                # Create a user using the parameters from the CSV
                new_user = create_user(
                    username=username,
                    firstname=row.get('firstname'),
                    lastname=row.get('lastname'),
                    password=password,
                    email=row.get('email'),
                    faculty=row.get('faculty')
                )

                # Check if the user was successfully created
                if new_user:
                    print(f"User created: {row['firstname']} {row['lastname']}")
                else:
                    print(f"Failed to create user: {row['firstname']} {row['lastname']}")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {str(e)}")