"""Class Finder Flask Routes"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Classroom, User, ClassUser

from datetime import datetime

# This is how Flask knows what module to scan for things like routes
app = Flask(__name__)


app.secret_key = "tamandua"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def search():
    """Homepage is the Search page"""

    return render_template("search.html")


@app.route('/login')
def loginpage():
    """Page where users can log in"""

    return render_template("login.html")


@app.route('/create-profile')
def create_user_profile():
    """Takes teacher and/or student input for profile info"""

    return render_template('create-profile.html')


@app.route('/new-profile', methods=(["POST"]))
def new_profile_confirmation():
    """Messages that profile has been created"""

    email = request.form.get("email")
    username = request.form.get("username")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    password = request.form.get("password")
    isteacher = bool(request.form.get("optionsRadios"))
    bio = request.form.get("bio")

    existing_account = User.query.filter(User.email == email).first()
    # Can add or statement later

    if not existing_account and len(password) > 0:
        flash("Your account has been created!")
        user = User(email=email, username=username, fname=fname, lname=lname, 
            password=password, is_teacher=isteacher, bio=bio)
        #white is above vars, orange is db fieldnames
        db.session.add(user)
        db.session.commit()
        print "New user added"
        return redirect('/profile')

        # JS asks if exising account
        # returns T/F
    elif existing_account:
        flash("It looks like there's already an account under that email. Try again!")
        return redirect('/create-profile')
    else:
        flash("Oops, it looks like you forgot to add a password!")
        
        return redirect('/create-profile')


@app.route('/profile')
def profile():
    """Profile page with user information"""

    return render_template("profile.html")


@app.route('/search')
def search_classes():
    """Search Box and browsing/parameter ticking"""

    return render_template('search.html')


@app.route('/class-info')
def class_info():
    """Reveals information about a class. Such as: language, level, days, times, teacher, students"""

    # lat = Class.query.filter(class_id)
    # lng=get from db, I don't remember how
    
    return render_template("class-info.html")


@app.route('/create-class')
def create_class_form():
    """Take teacher input from class creation form"""
    
    return render_template('create-class.html')


@app.route('/teacherclass', methods=(["POST"]))
def class_submission():
    """Message that class has been created"""

    # This is where the create-class info is held as a post
    language = request.form.get("languagetype")
    level = request.form.get('leveltype')
    price = request.form.get('pricetype')
    min_students = request.form.get('min')
    max_students = request.form.get('max')
    days = str(request.form.get('days'))
    start_date = request.form.get('start')
    start_date = str(request.form.get('%A, %B, %d, %Y'))
    end_date = request.form.get('end')
    end_date = str(request.form.get('%A, %B, %d, %Y'))
    time = request.form.get('timetype')
    time = str(request.form.get('%H, %M'))

    print type(start_date)
    print type(end_date)
    print type(time)
    newclass = Classroom(language=language, level=level, cost=price, min_students=min_students, 
                        max_students=max_students, class_days=days, 
                        start_date=start_date, end_date=end_date, time=time)


    db.session.add(newclass)
    db.session.commit()

    return render_template("class-created.html")

    # This needs to be a post method
    # class then needs to be added to the class-info page
    # class needs to be searchable once posted



# FUTURE ROUTES!!!
    # Search Results
    # Profile page for student vs teacher
    # Payment

# Future Future Routes!
    # Student class creation page!








if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()