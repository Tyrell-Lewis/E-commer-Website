from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Student, Staff, User, Review

from App.controllers import (
    get_student_by_UniId, get_student_by_id,
    get_staff_by_id, get_staff_by_id, create_review, get_karma,
    calculate_ranks, get_reviews, get_review, edit_review_work, delete_review_work,
    create_comment, get_comment, get_comment_staff,
    get_reply, create_reply, get_all_reviews, create_staff, get_student_review_index, get_karma_history,
    like, dislike, update_staff_profile, get_all_students_json, get_staff_by_username, login_user)            #added get_reviews


staff_views = Blueprint('staff_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@staff_views.route('/edit-profile/<int:staff_id>', methods=['GET'])
def edit_staff_profile_route(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        flash("Staff not found.", "error")
        return redirect(request.referrer)

    return render_template('EditProfile.html', staff=staff)


@staff_views.route('/update-staff-profile', methods=['POST'])
def update_staff_profile_route():
    staff_id = request.form.get('staff_id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    faculty = request.form.get('faculty')
    email = request.form.get('email')
    profile_pic = request.files.get('profile_pic')

    try:
        # Assume this function updates everything and handles the image too
        update_staff_profile(
            staff_id=staff_id,
            firstname=firstname,
            lastname=lastname,
            faculty=faculty,
            email=email,
            profile_pic=profile_pic
        )

        flash("Profile updated successfully!", "success")
        return redirect(url_for('staff_views.staff_profile', staff_id=staff_id))
    except Exception as e:
        print(f"Error updating profile: {e}")
        flash("Something went wrong while updating the profile.", "error")
        return redirect(url_for('staff_views.getAllReviews'))



@staff_views.route('/like/<int:review_id>', methods=['POST'])
def like_review(review_id):
    like(review_id, current_user.get_id())
    return redirect(request.referrer)

@staff_views.route('/dislike/<int:review_id>', methods=['POST'])
def dislike_review(review_id):
    dislike(review_id, current_user.get_id())
    return redirect(request.referrer)

@staff_views.route('/students/<int:student_id>/reviews/<int:review_index>', methods=['GET'])
def review_detail(student_id, review_index):
    student = get_student_by_UniId(student_id)
    if student:
        if review_index in range(len(student.reviews)):
            review_id = student.get_review_id(review_index)
            review = get_review(review_id)
            if review:
                staff = get_staff_by_id(review.createdByStaffID)
                review.staff_name = f"{staff.firstname} {staff.lastname}" if staff else "Unknown Staff"
                review.student_name = student.fullname
                review.student_id = student.UniId
                review.staffpic = staff.profile_pic

                comment_staffs = []
                replier_staffs = []

                for comment in review.comments:
                    comment_staffs.append(get_comment_staff(comment.createdByStaffID))
                    
                    replier_list = []
                    for reply in comment.replies:
                        replier_list.append(get_comment_staff(reply.createdByStaffID))
                    replier_staffs.append(replier_list)

                comment_info = zip(review.comments, comment_staffs)
                return render_template('ReviewDetail.html', review=review, comment_info=comment_info, replier_staffs=replier_staffs, get_staff=get_staff_by_id)
            else:
                flash("Review does not exist", "error")
    else:
        flash("Student does not exist", "error")
    return redirect('/getMainPage')


@staff_views.route('/reviews/<int:review_id>', methods=['POST'])
@login_required
def post_comment(review_id):
  content = request.form
  review = get_review(review_id)
  if current_user.user_type == 'staff':
    details = content['details']
    details = "\n".join(textwrap.wrap(details, width=80))  # Wrap text at 80 characters

    create_comment(review_id, current_user.ID, details)
    return redirect(f"/reviews/{review.ID}")
  else:
     flash("Must be logged in as staff", "error")
     return redirect('/login')

@staff_views.route('/reviews/<int:review_id>', methods=['GET'])
@login_required
def expand_review(review_id):
  review = get_review(review_id)
  if review:
    student = get_student_by_id(review.studentID)
    review_index = get_student_review_index(student.ID, review.ID)
    return redirect(f"/students/{student.UniId}/reviews/{review_index}")
  else:
     flash("Review does not exist", "error")
     return redirect('/getMainPage')

@staff_views.route('/comments/<int:comment_id>', methods=['POST'])
@login_required
def post_reply(comment_id):
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)
  if staff:
    data = request.form
    details = data['reply-details']
    details = "\n".join(textwrap.wrap(details, width=80))  # Wrap text at 80 characters

    comment = get_comment(comment_id)

    if comment:
        create_reply(commentID=comment_id, staffID=staff_id, details=details, parentReplyID=None)
        return redirect(f"/reviews/{comment.reviewID}")
    else:
        error = f"Comment is not found!"
  else:
    error = f"You are not logged in as staff and cannot post a Reply!"
  flash(error, "error")
  return redirect('/getMainPage')
   
@staff_views.route('/mainReviewPage', methods=['GET'])
def mainReviewPage():
  return render_template('CreateReview.html')

@staff_views.route('/createReview', methods=['POST'])
@login_required
def createReview():
    staff_id = current_user.get_id()
    staff = get_staff_by_id(staff_id)

    data = request.form
    studentID = data['studentID']
    studentName = data['name']
    points = int(data['points'])
    num = data['num']
    personalReview = data['manual-review']
    details = data['selected-details']

    # Ensure studentName is valid before splitting
    if ' ' in studentName:
        firstname, lastname = studentName.split(' ', 1)
    else:
        firstname, lastname = studentName, ""

    student = get_student_by_UniId(studentID)

    if personalReview:
        wrapped_review = "\n".join(textwrap.wrap(personalReview, width=80))  # Wrap text at 80 characters
        details += f"{wrapped_review}"
        points += int(data.get('starRating', 0))  # Ensure default value if missing

    positive = points > 0  # Determine review positivity

    if student:
        review = create_review(staff, student, points, details)
        flash(f"Successfully created a review for {studentName}!", "success")
    else:
        flash(f"Error creating review for {studentName}. Please check student details.", "error")

    return redirect(request.referrer)  # Redirect to the create review page

@staff_views.route('/deleteReview/<int:review_id>', methods=['GET'])
@login_required
def delete_review(review_id):
  review = get_review(review_id)

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  if review:
    delete_review_work(review_id=review_id, staff_id=staff_id) 
    flash(f"Successfully deleted review!", "success")
  else:
    flash(f"Error deleting review.", "error")

  return redirect(url_for('staff_views.getAllReviews'))# Put the appropriate template here, and current_user if needed.




@staff_views.route('/editReview/<review_id>', methods=['POST'])
@login_required
def edit_review(review_id):
  review = get_review(review_id)

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  data = request.form
  points = int(data['points'])
  num = data['num']
  personalReview = data['manual-review']
  details = data['selected-details']

  starRating = data['selectedRating']

  if personalReview:
        details += f"{personalReview}"
        points += int(data.get('starRating', 0))  # Ensure default value if missing

  if review:
    edit_review_work(details=details, review_id=review_id, staff_id=staff_id, starRating=starRating)
    print("work")
    flash(f"Successfully edited review!", "success")
  else:
    flash(f"Error editing review for {review_id}. Please check student details.", "error")

  return redirect(url_for('staff_views.getAllReviews'))# Put the appropriate template here, and current_user if needed.


@staff_views.route('/createReviewPage', methods=['GET'])
@login_required
def create_review_page():
    return render_template('CreateReview.html')


@staff_views.route('/editReviewPage/<id>', methods=['GET'])
@login_required
def edit_review_page(id):

  sel_review = get_review(id)

  sel_student = get_student_by_id(sel_review.studentID)

  return render_template('EditReview.html', sel_review= sel_review, sel_student=sel_student)

@staff_views.route('/students')
@staff_views.route('/students/<int:uni_id>')
@login_required
def view_students(uni_id=-1):
  students = get_all_students_json()
  if students:
    if uni_id == -1:
      selected_student = get_student_by_id(students[0]['id'])
    else:
      selected_student = get_student_by_UniId(uni_id)
  else:
    

    selected_student = None


   
  if selected_student:
    karma = get_karma(selected_student.ID)


  karma_history = get_karma_history(selected_student.ID)

  if not karma_history:
    karma_history = []
    
  reviews = selected_student.reviews
  
  if reviews:
     for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname
        review.staffpic = staff.profile_pic
  
  if reviews is None:
    reviews = []
  

 
  review_links = []
  for review in reviews:
      index = get_student_review_index(selected_student.ID, review.ID)
      review_links.append(index)

  students.sort(key = lambda e: e['firstname'])
  return render_template('AllStudents.html', students=students, selected_student=selected_student, reviews=reviews, karma=karma, history = karma_history, review_links = review_links, student=selected_student,)
  
@staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
@login_required
def getStudentProfile(uniID):
    student = Student.query.filter_by(UniId=uniID).first()

    if student is None:
        student = Student.query.filter_by(ID=uniID).first()

    user = User.query.filter_by(ID=student.ID).first()
    karma = get_karma(student.ID)

    if karma:
        calculate_ranks()

    reviews = get_reviews(student.ID)

    karma_history = get_karma_history(student.ID)

    # Attach staff name dynamically
    for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname
        review.staffpic = staff.profile_pic

    review_links = []
    for review in reviews:
        index = get_student_review_index(student.ID, review.ID)
        review_links.append(index)


    return render_template('Student-Profile-forStaff.html',
                           student=student,
                           user=user,
                           karma=karma,
                           reviews=reviews,
                           history = karma_history,
                           review_links = review_links)

@staff_views.route('/getMainPage', methods=['GET'])
@login_required
def getAllReviews():
    
    reviews = get_all_reviews()

    # Attach staff name dynamically
    for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname
        review.staffpic = staff.profile_pic

    for review in reviews:
        student = get_student_by_id(review.studentID)
        review.student_name = student.fullname if student else "Unknown Student"  # Attach fullname
        review.student_id = student.UniId if student else "Unknown ID"

    return render_template('MainPage.html',
                           reviews=reviews, current_user=current_user)

@staff_views.route('/staff-profile', methods=['GET'])
@login_required
def staff_profile():
    staff_id = current_user.get_id()  # Get logged-in staff ID
    staff = get_staff_by_id(staff_id)  # Fetch staff details

    if not staff:
        flash("Staff not found.", "error")
        return redirect(url_for('staff_views.get_StaffHome_page'))

    # Fetch reviews written by this staff member
    reviews = Review.query.filter_by(createdByStaffID=staff_id).all()

    # Create a list of formatted student names corresponding to each review
    student_names = []
    for review in reviews:
        student = get_student_by_id(review.studentID)
        if student:
            student_names.append(f"{student.fullname} ({student.UniId})")
        else:
            student_names.append("Unknown Student")

    return render_template('StaffProfile.html', staff=staff, reviews=reviews, student_names=student_names)

@staff_views.route('/staff-profile/<int:ID>', methods=['GET', 'POST'])
@login_required
def staff_profile_by_id(ID):
    staff = get_staff_by_id(ID)  # Fetch staff details

    if not staff:
        flash("Staff not found.", "error")
        return redirect(url_for('staff_views.get_StaffHome_page'))

    # Fetch reviews written by this staff member
    reviews = Review.query.filter_by(createdByStaffID=ID).all()

    # Create a list of formatted student names corresponding to each review
    student_names = []
    for review in reviews:
        student = get_student_by_id(review.studentID)
        if student:
            student_names.append(f"{student.fullname} ({student.UniId})")
        else:
            student_names.append("Unknown Student")

    return render_template('StaffProfile.html', staff=staff, reviews=reviews, student_names=student_names)

@staff_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        faculty = request.form['faculty']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        temp_user = get_staff_by_username(username)

        if temp_user:
          return render_template('SignUp.html', message="Username is already taken!")

        if password != confirm_password:
            return render_template('SignUp.html', message="Passwords do not match!")

        # Save user to the database
        create_staff(
            firstname=firstname, lastname=lastname,
            faculty=faculty, username=username,
            email=email, password=password
        )

        staff = get_staff_by_username(username)
 
        login_user(staff)

        return redirect("/getMainPage") # Redirect to login after signup

    return render_template('SignUp.html')



@staff_views.route('/jsreview/<int:review_id>', methods=['GET'])
@login_required
def js_review_detail(review_id):
    # Retrieve the review using its ID
    review = get_review(review_id)
    if not review:
        flash("Review not found.", "error")
        return redirect(url_for('staff_views.getAllReviews'))
    
    # Retrieve the associated student using the correct attribute name:
    student = get_student_by_id(review.studentID)  # Use 'studentID' here
    if not student:
        flash("Associated student not found.", "error")
        return redirect(url_for('staff_views.getAllReviews'))
    
    # Retrieve the staff member who created the review and attach their full name.
    staff_member = get_staff_by_id(review.createdByStaffID)
    review.staff_name = f"{staff_member.firstname} {staff_member.lastname}" if staff_member else "Unknown Staff"
    
    # Attach the student's full name for display in the template.
    review.student_name = student.fullname if student else "Unknown Student"
    # IMPORTANT: Set review.student_id (used in your template link) to the student's UniId.
    review.student_id = student.UniId
    
    # Format the review date if needed.
    if review.dateCreated:
        review.dateCreated = review.dateCreated.strftime('%Y-%m-%d %H:%M:%S')
    
    # Render the ReviewDetail page using your provided template.
    return render_template('ReviewDetail.html', review=review)


@staff_views.route('/search-students', methods=['GET'])
def search_students():
    query = request.args.get('q', '')
    students = Student.query.filter(
        (Student.firstname.ilike(f'%{query}%')) |
        (Student.lastname.ilike(f'%{query}%')) |
        ((Student.firstname + ' ' + Student.lastname).ilike(f'%{query}%'))
    ).all()

    results = [{
        "id": s.UniId,
        "name": f"{s.firstname} {s.lastname}"
    } for s in students]

    return jsonify(results)


@staff_views.route('/get_student_name', methods=['POST'])
def get_student_name():
    student_id = request.json['studentID']

    student = get_student_by_UniId(student_id)

    return jsonify({'studentName': student.fullname})


@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():
    return render_template('StudentSearch.html')


@staff_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
    return render_template('ReviewSearch.html')