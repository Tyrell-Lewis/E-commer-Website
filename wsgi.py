import click, pytest, sys
# import csv
from flask import current_app
from flask import Flask
from flask.cli import with_appcontext, AppGroup
import subprocess

from App.database import db, get_migrate
from App.main import create_app
from App.models import Customer
from App.models import User

from App.controllers import(
    initialize,
    create_customer
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():

    initialize()
    print ("Database initialized!")


  
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



# @test.command("perf", help="Run performance tests")
# @click.argument("target", default="all") 
# @click.option("--users", default=30, help="Number of concurrent users to simulate.")
# @click.option("--ramp", default=5, help="Rate at which users are spawned (users per second).")
# @click.option("--duration", default="30s", help="Run time duration")
# def performance_tests_command(target, users, ramp, duration):
#     locust_file_map = {
#         "login": "App/tests/locust_login.py",
#         "home": "App/tests/locust_home.py",
#         "create_review": "App/tests/locust_createReview.py",
#         "edit_review": "App/tests/locust_editReview.py",
#         "create_comment": "App/tests/locust_createComment.py",
#         "create_reply": "App/tests/locust_createReply.py",
#         "like_review": "App/tests/locust_likeReview.py",
#         "dislike_review": "App/tests/locust_dislikeReview.py",
#         "student": "App/tests/locust_student.py",
#     }

#     if target == "all":
#         for name, file in locust_file_map.items():
#             print(f"Running performance test: {name}")
#             subprocess.run([
#                 "locust", "-f", file, "--headless", "-u", str(users), "-r", str(ramp),
#                 "--host", "https://8080-500brainnot-studentcond-t8aifwj4lfk.ws-us118.gitpod.io/", "--run-time", duration, #Gitpod url: https://8080-500brainnot-studentcond-0z6711a4bxh.ws-us118.gitpod.io
#                 "--csv", f"perf_results/{name}"
#             ])
#     elif target in locust_file_map:
#         file = locust_file_map[target]
#         subprocess.run([
#             "locust", "-f", file, "--headless", "-u", str(users), "-r", str(ramp),
#             "--host", "https://8080-500brainnot-studentcond-t8aifwj4lfk.ws-us118.gitpod.io/", "--run-time", duration, #Gitpod url: https://8080-500brainnot-studentcond-0z6711a4bxh.ws-us118.gitpod.io
#             "--csv", f"perf_results/{target}" 
#         ])
#     else:
#         print(f"Unknown performance target: {target}")


app.cli.add_command(test)