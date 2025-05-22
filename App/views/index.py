from flask import Blueprint, render_template, jsonify, flash, send_from_directory, redirect, url_for
from App.models import db
from App.controllers import (
  get_all_items
)

index_views = Blueprint('index_views',
                        __name__,
                        template_folder='../templates')


@index_views.route('/', methods=['GET'])
def index_page():
  
  
  return redirect("/Home")

@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()

  return jsonify(message='db initialized!')


@index_views.route('/healthcheck', methods=['GET'])
def health_check():
  return jsonify({'status': 'healthy'})