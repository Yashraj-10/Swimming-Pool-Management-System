
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from pkg_resources import Requirement
from urllib3 import PoolManager
from . import db,addAdmin
from .models import User, Competition, Post, Ticket, Course
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/viewcourses', methods=['GET', 'POST'])
@login_required
def viewcourses():
    courses=Course.query.all()
    return render_template('view.html',views=courses)
@views.route('/membership', methods=['GET', 'POST'])
@login_required
def membership():
    if(request.method == 'POST'):

        data = request.form

        user = User.query.filter_by(id=current_user.id).first()
        user.contactNumber = data['contactNumber']
        user.address = data['address']
        
        user.membershipstatus = 'pending'

        db.session.commit()

        flash("Successfully applied", category='success')

        return redirect(url_for('views.dashboard'))

    return render_template('membership.html')


@views.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    if(request.method == 'POST'):

        data = request.form

        user = User.query.filter_by(id=current_user.id).first()
        user.contactNumber = data['contactNumber']
        user.address = data['address']
        

        db.session.commit()
        flash("Successfully applied", category='success')

        return redirect(('/viewcourses'))
    return render_template('courses.html')


@views.route('/competition', methods=['GET', 'POST'])
@login_required
def competition():
    if(request.method == 'POST'):

        data = request.form

        user = User.query.filter_by(id=current_user.id).first()
        user.contactNumber = data['contactNumber']
        user.address = data['address']
        user.document = data['document']

        db.session.commit()
        flash("Successfully applied", category='success')

        return redirect(url_for('views.dashboard'))
    return render_template('competition.html')


@views.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    if request.method == 'GET':

        competition = Competition.query.all()
        return render_template('view_competition.html', competitions=competition)


@views.route('/usercourses', methods=['GET', 'POST'])
@login_required
def user_courses():

    return render_template('user_courses.html', courses=current_user.courses)


@views.route('/usercompetition', methods=['GET', 'POST'])
@login_required
def user_competition():
    return render_template('user_competition.html', competitions=current_user.competitions)


@views.route('/usernotification', methods=['GET', 'POST'])
@login_required
def user_notification():
    return render_template('user_notification.html', notifications=current_user.posts)

@views.route('/usernotice', methods=['GET', 'POST'])
@login_required
def notice():
    return render_template('usernotice.html',notice=current_user.posts)

@views.route('/userpost', methods=['GET', 'POST'])
@login_required
def user_post():
    

    
    return render_template('userpost.html', posts=Post.query.filter_by(type='public').all())

@views.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    return render_template('payment.html')
@views.route('/accountdetails', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('accountdetails.html',user=current_user)
@views.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    if request.method=='POST':
        data=request.form
        if(data['password']==data['password2']):
            # flash('Signup Successful',category='success')
            
            # user=User()
            user=User(name=data['name'],email=data['email'],password=generate_password_hash(data['password']),type=data['type'])

            db.session.add(user)
            db.session.commit()
            login_user(user,remember=True)
            print("User added")
            print(user)

            
            return redirect(url_for('views.dashboard'))


        else:

            
            flash('Password and Confirm Password must be same',category='error')
            return redirect(url_for('auth.signup'))
    return render_template('adduser.html')
@views.route('/addcourse', methods=['GET', 'POST'])
@login_required
def addcourse():
    if request.method=='POST':
        data=request.form
        course=Course(name=data['name'],price=data['price'],duration=data['duration'],date=data['date'],requirements=data['requirements'])
        course.courseCoordinatorId=current_user.id
        print(course)
        db.session.add(course)
        return redirect(url_for('views.Admin_dashboard'))
        db.session.commit()
    
    return render_template('addcourse.html')

@views.route('/addcompetition', methods=['GET', 'POST'])
@login_required
def addcompetition():
    if request.method=='POST':
        data=request.form
        competition=Competition(name=data['name'],format=data['format'],date=data['date'])
        print(competition)
        db.session.add(competition)
        return redirect(url_for('views.Admin_dashboard'))
        db.session.commit()
    
    return render_template('addcompetition.html')

@views.route('/cancelmember', methods=['GET', 'POST'])
@login_required
def cancelmember():
    if request.method=='POST':
        data=request.form
        print(data['reason'])
        PoolManagers=User.query.filter_by(type='poolmanager').all()

        post=Post(title='Notification',content=data['reason'])
        
        for  poolmanager in PoolManagers:
            print(poolmanager)
            poolmanager.posts.append(post)
            print(poolmanager.posts)
            db.session.commit()
        

        current_user.type='user'
        print(data)
        return redirect('dashboard')
        
        
    
    return render_template('cancelmember.html')
@views.route('/viewnotif', methods=['GET', 'POST'])
@login_required
def viewnotifs():
    print(current_user.posts)
    print(current_user)
    return render_template('view.html',views=current_user.posts)

@views.route('/viewusers', methods=['GET', 'POST'])
@login_required
def viewusers():
    users=User.query.all()
    print(users)
    return render_template('view.html',views=users)

@views.route('/viewcompetitions', methods=['GET', 'POST'])
@login_required
def viewcompetitions():
    competitions=Competition.query.all()
    return render_template('view.html',views=competitions)
@views.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method=='POST':
        data=request.form
        print(data)
        post=Post(title=data['title'],content=data['content'],type=data['type'])
        post.user_id=current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('views.dashboard'))
    return render_template('post.html')
@views.route('/approvemembership', methods=['GET', 'POST'])
@login_required
def approvemembership():
    users=User.query.filter_by(membershipstatus='pending').all()
    for user in users:
        print(user.membershipstatus)
    return render_template('view.html',views=users)
    

########Dashboard#############
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if(current_user.type=='admin'):
        return render_template('Admin_dashboard.html')
    elif(current_user.type=='member'):
        return render_template('member_dashboard.html')
    elif(current_user.type=='user'):
        return render_template('user_dashboard.html')
    elif(current_user.type=='coursecoordinator'):
        return render_template('courseCor__dashboard.html')
    elif(current_user.type=='poolmanager'):
        return render_template('poolman_dashboard.html')
    elif(  current_user.type=='poolmanagementcommittee'):
        return render_template('poolmancom_dashboard.html')
    else:
        return render_template('eventman_dashboard.html')

