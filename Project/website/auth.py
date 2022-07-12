from flask import Blueprint,render_template,request,redirect,url_for,flash
from .models import User,Post,Ticket,Competition
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,logout_user,login_required,current_user
auth=Blueprint('auth',__name__)
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        data=request.form
        print(data)

        
        
        user=User.query.filter_by(email=data['email']).first()
        if user:
            if check_password_hash(user.password,data['password']):
                login_user(user,remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Invalid Password',category='error')
        else:
            flash('Invalid Email',category='error')
            # return redirect(url_for('views.home'))
     
        
        

      
    return render_template('login.html',text='Login')
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')
@auth.route('/sign-up',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        data=request.form
        if(data['password']==data['password2']):
            # flash('Signup Successful',category='success')
            print(type(data['password']))
            # user=User()
            user=User(name=data['name'],email=data['email'],password=generate_password_hash(data['password']),type='user')

            db.session.add(user)
            db.session.commit()
            login_user(user,remember=True)
            print("User added")
            print(user)
            
            return redirect(url_for('views.dashboard'))

        else:

            
            flash('Password and Confirm Password must be same',category='error')
            return redirect(url_for('auth.signup'))
    
      
    
    return render_template('sign_up.html')

