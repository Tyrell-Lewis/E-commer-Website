import click, pytest, sys
import csv
from flask import current_app
from flask import Flask
from flask.cli import with_appcontext, AppGroup
import subprocess

from App.database import db, get_migrate
from App.main import create_app
from App.models import Student, Karma, Comment
from App.models import User
from App.controllers import (
    create_student, create_staff, create_admin, get_all_users_json,
    get_all_users, 
    #get_transcript, 
    get_student_by_UniId, 
    #get_total_As, get_total_courses_attempted,
    #calculate_academic_score, 
    create_review, 
    #create_incident_report,
    #create_accomplishment, 
    get_staff_by_id, get_student_by_id,
    #create_job_recommendation, 
    create_karma, get_karma, 
    #create_badge, 
    calculate_ranks,
    #get_accomplishments_by_studentID, 
    get_staff_by_name, create_comment, delete_student,
    update_student)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()

  create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="")

  create_student(username="shivum",
                 firstname="Shivum",
                 lastname="Praboocharan",
                 email="shivum.praboocharan@my.uwi.edu",
                 password="shivumpass",
                 faculty="FST",
                 admittedTerm="2019/2021",
                 UniId='816016480',
                 degree="Bachelor of Computer Science with Management",
                 gpa='')

  create_student(username="jovani",
                 firstname="Jovani",
                 lastname="Highley",
                 email="jovani.highley@my.uwi.edu",
                 password="jovanipass",
                 faculty="FST",
                 admittedTerm="2021/2022",
                 UniId='816026834',
                 degree="Bachelor of Computer Science with Management",
                 gpa='')

  create_student(username="kasim",
                 firstname="Kasim",
                 lastname="Taylor",
                 email="kasim.taylor@my.uwi.edu",
                 password="kasimpass",
                 faculty="FST",
                 admittedTerm="2019/2021",
                 UniId='816030847',
                 degree="Bachelor of Computer Science (General)",
                 gpa='')

  create_student(username="brian",
                 firstname="Brian",
                 lastname="Cheruiyot",
                 email="brian.cheruiyot@my.uwi.edu",
                 password="brianpass",
                 faculty="FST",
                 admittedTerm="2021/2022",
                 UniId='816031609',
                 degree="Bachelor of Computer Science (General)",
                 gpa="")

  #Creating staff
  create_staff(username="tim",
               firstname="Tim",
               lastname="Long",
               email="",
               password="timpass",
               faculty="")

  create_staff(username="vijay",
               firstname="Vijayanandh",
               lastname="Rajamanickam",
               email="Vijayanandh.Rajamanickam@sta.uwi.edu",
               password="vijaypass",
               faculty="FST")

  create_staff(username="permanand",
               firstname="Permanand",
               lastname="Mohan",
               email="Permanand.Mohan@sta.uwi.edu",
               password="password",
               faculty="FST")


  staff = get_staff_by_id(7)
  student1 = get_student_by_UniId(816031609)
  review1 = create_review(staff, student1, 5, "Behaves very well in class!")
  create_review(staff, student1, 2, "Late to class")
  create_review(staff, student1, 5, "Good CW grades")
  create_review(staff, student1, 3, "Okay Final grades")

  student2 = get_student_by_UniId(816016480)
  create_review(staff, student2, 5, "Behaves very well in class!")
  student3 = get_student_by_UniId(816026834)
  create_review(staff, student3, 3, "Behaves very well in class!")
  student4 = get_student_by_UniId(816030847)
  create_review(staff, student4, 5, "Behaves very well in class!")
  create_admin(username="admin",
               firstname="Admin",
               lastname="Admin",
               email="admin@example.com",
               password="password",
               faculty="FST")

  students = Student.query.all()

  
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("unit", help="Run all Unit tests")
def all_tests_command():
    sys.exit(pytest.main(["-k", "UnitTests"]))


@test.command("int", help="Run all Integration tests")
def all_tests_command():
    sys.exit(pytest.main(["-k", "IntegrationTests"]))

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Student"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Staff"]))


@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Review"]))



@test.command("comment", help="Run Comment tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CommentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CommentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Comment"]))



@test.command("reply", help="Run Reply tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReplyUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReplyIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Reply"]))



@test.command("karma", help="Run Karma tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Karma"]))



@test.command("perf", help="Run performance tests")
@click.argument("target", default="all") 
@click.option("--users", default=30, help="Number of concurrent users to simulate.")
@click.option("--ramp", default=5, help="Rate at which users are spawned (users per second).")
@click.option("--duration", default="30s", help="Run time duration")
def performance_tests_command(target, users, ramp, duration):
    locust_file_map = {
        "login": "App/tests/locust_login.py",
        "home": "App/tests/locust_home.py",
        "create_review": "App/tests/locust_createReview.py",
        "edit_review": "App/tests/locust_editReview.py",
        "create_comment": "App/tests/locust_createComment.py",
        "create_reply": "App/tests/locust_createReply.py",
        "like_review": "App/tests/locust_likeReview.py",
        "dislike_review": "App/tests/locust_dislikeReview.py",
        "student": "App/tests/locust_student.py",
    }

    if target == "all":
        for name, file in locust_file_map.items():
            print(f"Running performance test: {name}")
            subprocess.run([
                "locust", "-f", file, "--headless", "-u", str(users), "-r", str(ramp),
                "--host", "https://8080-500brainnot-studentcond-t8aifwj4lfk.ws-us118.gitpod.io/", "--run-time", duration, #Gitpod url: https://8080-500brainnot-studentcond-0z6711a4bxh.ws-us118.gitpod.io
                "--csv", f"perf_results/{name}"
            ])
    elif target in locust_file_map:
        file = locust_file_map[target]
        subprocess.run([
            "locust", "-f", file, "--headless", "-u", str(users), "-r", str(ramp),
            "--host", "https://8080-500brainnot-studentcond-t8aifwj4lfk.ws-us118.gitpod.io/", "--run-time", duration, #Gitpod url: https://8080-500brainnot-studentcond-0z6711a4bxh.ws-us118.gitpod.io
            "--csv", f"perf_results/{target}" 
        ])
    else:
        print(f"Unknown performance target: {target}")





app.cli.add_command(test)


# ---- CLI commands ---- #

# 1 add admin user

@app.cli.command('add_admin')
@click.argument('username')
@click.argument('firstname')
@click.argument('lastname')
@click.argument('email')
@click.argument('password')
@click.argument('faculty')
def add_admin(username, firstname, lastname, email, password, faculty):
    
    success = create_admin(username, firstname, lastname, email, password, faculty)
    if success:
        click.echo(f"Admin {username} created successfully!")
    else:
        click.echo(f"Failed to create admin {username}.")
        
        



@app.cli.command("add_student", help="Add a student manually")
@click.argument("uni_id", required=True)
@click.argument("first_name", required=True)
@click.argument("last_name", required=True)
@click.argument("email", required=True)
@click.argument("faculty", required=True)
@click.argument("admit_term", required=True)
@click.argument("degree", required=True)
@click.argument("gpa", required=True)
def add_student(uni_id, first_name, last_name, email, faculty, admit_term, degree, gpa):
    create_student("", uni_id, first_name, last_name, email, "", faculty, admit_term, degree, gpa)
    print(f"Created student {uni_id} successfully")

@app.cli.command("add_students", help="Add multiple students by specifying a CSV file")
@click.argument("path", required=True)
def add_students(path):
    with open(path, newline='') as student_csv:
        reader = csv.DictReader(student_csv)
        for student in reader:
            create_student("", student['uni_id'], student['first_name'], student['last_name'], student['email'], "", student['faculty'], student['admit_term'], student['degree'], student['gpa'])
        print("Added all students successfully")

@app.cli.command("edit_student", help="Edit a student record")
@click.argument("uni_id", required=True)
@click.argument("field", type=click.Choice(['first_name', 'last_name', 'email', 'faculty', 'admit_term', 'degree', 'gpa'], case_sensitive=False), required=True)
@click.argument("new_value", required=True)
def edit_student(uni_id, field, new_value):
    print(update_student(uni_id, field, new_value))

@app.cli.command("delete_student", help="Remove a student record")
@click.argument("uni_id", required=True)
def remove_student(uni_id):
    print(delete_student(uni_id))