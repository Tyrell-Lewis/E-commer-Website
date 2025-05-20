from flask import Blueprint, render_template, jsonify
from App.models import db, Student
# from App.controllers import (
#     create_student,
#     create_staff,
#     create_admin,
#     get_staff_by_id,
#     get_student_by_UniId,
#     create_review,
# )

index_views = Blueprint('index_views',
                        __name__,
                        template_folder='../templates')


@index_views.route('/', methods=['GET'])
def index_page():
  return render_template('login.html')

@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()

  return jsonify(message='db initialized!')


@index_views.route('/healthcheck', methods=['GET'])
def health_check():
  return jsonify({'status': 'healthy'})