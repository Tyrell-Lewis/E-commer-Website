from flask import Blueprint, render_template
from flask_login import login_required
from App.models import Student
from App.controllers import (calculate_ranks)

student_views = Blueprint('student_views',
                          __name__,
                          template_folder='../templates')
'''
Page/Action Routes
'''

@student_views.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard_api():
    # Retrieve all students
    students = Student.query.all()

    # Ensure students exist before proceeding
    if not students:
        return render_template('Leaderboard.html', students_json=[])

    # Recalculate karma points (ignoring rank)
    calculate_ranks()

    # Convert to JSON and get karma scores
    students_json = [
        stu.to_json(stu.get_karma()) for stu in students
    ]

    # Sort students by karma score (descending order)
    sorted_students = sorted(
        students_json,
        key=lambda x: x['karma_history'][-1]['score'] if x['karma_history'] else 0,
        reverse=True  # Highest karma first
    )

    # Generate ranks dynamically (1-based index)
    ranks = list(range(1, len(sorted_students) + 1))

    # Zip students and ranks together
    students_with_ranks = list(zip(sorted_students, ranks))

    # Pass it to the template
    return render_template(
        'Leaderboard.html',
        students_with_ranks=students_with_ranks
    )