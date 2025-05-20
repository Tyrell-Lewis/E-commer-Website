from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, login_user, logout_user

from App.controllers import (login)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''

@auth_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  message="Bad username or password"
  
  user = login(data['username'], data['password'])
  if user:
    user_type = type(user)
    print("User type:", user_type)
    login_user(user)
    if (user.user_type == "staff"):
      return redirect("/getMainPage")  # Redirect to student dashboard
    # elif (user.user_type == "student"):
    #   return redirect("/StudentHome")  # Redirect to staff dashboard
    # elif (user.user_type == "admin"):
    #   return redirect("/admin")
  return render_template('login.html', message=message)


@auth_views.route('/logout', methods=['GET'])
@login_required
def logout_action():
  logout_user()
  # data = request.form
  # user = login(data['username'], data['password'])
  #return 'logged out!'
  return redirect("/")