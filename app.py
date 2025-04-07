from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
from all_sampledata import sample_jobs,posted_jobs, current_user

app = Flask(__name__)
#DATABASE 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../job_search/app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Profils finish
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROFILE_PHOTOS'] = 'profile_photos'
app.config['RESUMES'] = 'resumes'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

class User_profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    user = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    passw = db.Column(db.String(50), unique=False, nullable=False)
    
    def __repr__(self):
        return f"Profiles('{self.id}', '{self.email}', '{self.passw}')"

class jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    expirience = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Jobs('{self.title}', '{self.expirience}')"
    
# Create the database
with app.app_context():
    db.create_all()

applications = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
           
@app.route('/profile')
def profile():
    if current_user['role'] == 'recruiter':
        return render_template('profile.html', user=current_user, posted_jobs=posted_jobs)
    else:
        return render_template('profile.html', user=current_user, applications=applications)
    
@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Update user data
    current_user['name'] = request.form['name']
    current_user['email'] = request.form['email']
    current_user['phone'] = request.form['phone']
    current_user['location'] = request.form['location']
    current_user['headline'] = request.form['headline']
    current_user['education'] = request.form['education']
    current_user['skills'] = request.form['skills']
    current_user['bio'] = request.form['bio']
    
    # Handle profile photo upload
    if 'profile_photo' in request.files:
        file = request.files['profile_photo']
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(f"user_{current_user['id']}.{file.filename.rsplit('.', 1)[1].lower()}")
            file.save(os.path.join(app.config['PROFILE_PHOTOS'], filename))
            current_user['profile_photo'] = filename
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('profile'))
    
    file = request.files.get('resume')
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('profile'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{current_user['id']}_resume.pdf")
        file.save(os.path.join(app.config['RESUMES'], filename))
        current_user['resume_filename'] = filename
        flash('Resume uploaded successfully!', 'success')
    else:
        flash('Only PDF files are allowed', 'error')
    
    return redirect(url_for('profile'))

@app.route('/view_resume/<filename>')
def view_resume(filename):
    return send_from_directory(app.config['RESUMES'], filename, as_attachment=False)

username = ""
password = ""
id = 0
sign = False

@app.route('/')
def home():
    return render_template('index.html',username = username,jobs = sample_jobs,sign=sign)

@app.route('/search', methods=['POST'])
def search_jobs():
    position = request.form.get('position', '').lower()
    experience = request.form.get('experience', '')
    cities = request.form.get('cities', '')
    location_type = request.form.get('location', 'onsite')
    # Filter jobs based on criteria
    filtered_jobs = []
    for job in sample_jobs:
        matches = True
        
        # Position filter
        if position and position not in job['title'].lower():
            matches = False
            
        # Experience filter
        if experience and job['experience'] != experience:
            matches = False
            
        # Location filter
        if location_type == 'onsite':
            if job['remote'] or (cities and job['location'] not in cities.split(',')):
                matches = False
        else:  # remote
            if not job['remote']:
                matches = False
                
        if matches:
            filtered_jobs.append(job)
    
    return render_template('index.html', jobs=filtered_jobs,sign=sign)

@app.route('/create-job')
def create_job():
    return "Job creation page would go here"

@app.route('/apply', methods = ['POST', 'GET'])
def apply():
    jobtitle = request.form.get('job_title')
    company_name = request.form.get('company_name')
    print(jobtitle,'\t',company_name)
    return render_template("apply.html")

@app.route('/contact')
def contact():
    return render_template('Conatct.html', sign=sign)

@app.route('/signin',methods=['GET', 'POST'])
def signin():
    email1 = request.form.get("emails")
    password_get = request.form.get("password1")
    user = User_profiles.query.filter_by(email=email1).first()
    if user and user.passw == password_get:
        username = user.user
        password = user.passw
        id = user.id
        sign=True
        current_user['id'] = id
        current_user['name'] = username
        current_user['email'] = email1
        current_user['phone'] = user.phonenumber
        return render_template('index.html',username = username,jobs = sample_jobs,sign=sign)
    elif(email1 != None or password_get != None):
        return render_template('sign_in.html', signtext = "wrong email and password")
    return render_template('sign_in.html', signtext = "")

def checkemailname(email):
    if(User_profiles.query.filter_by(email=email).first()):
        print(User_profiles.query.filter_by(email=email).first())
        return True
    else:
        return False

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    Full_name = request.form.get("fullname")  # Matches 'fullname' in HTML
    usernamein = request.form.get('username')  # Matches 'username' in HTML
    email1 = request.form.get('email1')  # Matches 'email1' in HTML
    phonenum = request.form.get("phonenumber")  # Matches 'phonenumber' in HTML
    password1 = request.form.get('password1')  # Matches 'password1' in HTML
    password2 = request.form.get('password2')  # Matches 'password2' in HTML
    print( Full_name , "\t", usernamein ,"\t", email1, "\t", phonenum, "\t", password1, '\t', password2)
     # Check if email is already used
    if checkemailname(email1) and email1 != None:
        return render_template('sign_up.html', signtext="Email already used")
    # Check if passwords match
    elif  password2 != None and password1 != password2:
        return render_template('sign_up.html', signtext="Passwords do not match")
    # Validate phone number length
    elif len(phonenum) < 10:  # Ensure phonenum is not None
        return render_template('sign_up.html', signtext="Invalid phone number") 
    # Check if all fields are filled
    elif all([Full_name, usernamein, email1, phonenum, password1]):
        global username, password, emailby_use,sign
        # new_user = User_profiles(full_name=Full_name, user = usernamein, email=emailby_use, phonenumber=phonenum, passw=password1)
        # db.session.add(new_user)
        # db.session.commit()
        # flash('your signup completed', 'success')
        from sqlalchemy.exc import IntegrityError
        try:
            new_user = User_profiles(full_name=Full_name, user=usernamein, email=emailby_use, phonenumber=phonenum, passw=password1)
            db.session.add(new_user)
            db.session.commit()
            username = usernamein
            emailby_use = email1
            password = password1
            sign = True
            flash('Your signup completed', 'success')
            current_user['id'] = id
            current_user['name'] = usernamein
            current_user['email'] = email1
            current_user['phone'] = phonenum
        except IntegrityError as e:
            db.session.rollback()  # Undo the transaction
            flash('some problem show it', 'error')
            return render_template('sign_up.html', signtext=e)
        return render_template('index.html', username=username, jobs=[], sign=sign)

    return render_template('sign_up.html', signtext="")

@app.route('/logout')
def logout():
    sign=False
    password = ''
    username = ''
    current_user['id'] = ''
    current_user['name'] = ''
    current_user['email'] = ''
    current_user['phone'] = ''
    return render_template('index.html', username=username, jobs=sample_jobs, sign=sign)
if __name__ == '__main__':
    app.run(debug=True)