"""Class Finder Flask Routes"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
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

    return render_template("home.html")


@app.route('/login')
def loginpage():
    """Page where users can log in"""

    return render_template("login.html")



@app.route('/login-success', methods=["POST"])
def check_login():
    """Checks info and logs user in to session"""

    # Flask Post
    email = request.form.get("email")
    password = request.form.get("password")

    # all_users = User.query.all()
    # print all_users

    user_account = User.query.filter_by(email=email, password=password).first()
    print user_account
    user_username = user_account.username
    print user_username

    # print "user_account.email:" + user_account.email

    if user_account:
        print user_account
        session["user_id"] = user_account.user_id
        print session["user_id"]
        return render_template("login-success.html", user_account=user_account, user_username=user_username)
    # else:
    #     flash("Wrong email or password, try again")
    #     return redirect ("/login")

    # elif email == user_account:
    #         flash("That email is invalid.")
    #         return redirect('/login')
    # elif password != user_account:
    #     flash("That password is invalid.")
    #     return redirect('/login')



@app.route('/create-profile')
def create_user_profile():
    """Takes teacher and/or student input for profile info"""

    return render_template('create-profile.html')


@app.route('/new-profile', methods=["POST"])
def new_profile_confirmation():
    """Messages that profile has been created"""

    # Flask Post

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

        user = User(email=email, username=username, fname=fname, lname=lname, 
            password=password, is_teacher=isteacher, bio=bio)
        #white is above vars, orange is db fieldnames
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.user_id

        print "New user added"
        print session["user_id"]
        return redirect('/profile')

        # JS asks if exising account
        # returns T/F
    elif existing_account:
        flash("It looks like there's already an account under that email. Try again!")
        return redirect('/create-profile')
    else:
        flash("Oops, it looks like you forgot to add a password!")
        
        return redirect('/create-profile')


@app.route('/profile/<user_username>')
def profile(user_username):
    """Profile page renders user information if user is logged in"""


    session_id = session["user_id"]
    print "session_id"
    print session_id

    user_email = db.session.query(User).filter(User.user_id == session_id).first()
    print "user_email"
    print user_email

    user_classes = db.session.query(Classroom).join(ClassUser).filter(ClassUser.user_id == session_id).all()
    print user_classes
    print "bonitinha"

    # class_list = user_classes.language
    # print class_list

    # for in_class in user_classes:
    #     print "in_class"
    #     print in_class


    return render_template("profile.html", user_email=user_email, user_classes=user_classes)


@app.route('/logout')
def logout():
    """Logout button and session end"""

    session.clear()

    return render_template("goodbye.html")



@app.route('/search')
def search_classes():
    """Search Box and browsing/parameters"""

    user_email = db.session.query(User).filter(User.user_id == session["user_id"]).first()

    user_username = user_email.username

    return render_template('search.html', user_username=user_username)


@app.route('/search-results', methods=["GET"])
def search_by_lang():
    """Search Results for Language and Level"""

    # Gets language input from dropdown in search.html
    languagetype = request.args.get("languagetype")
    leveltype = request.args.get("leveltype")
    # print languagetype

    lang_result = db.session.query(Classroom.class_id, Classroom.language).all()


    # gives me a list of objects
    spec_results = db.session.query(Classroom).filter(Classroom.language==languagetype, Classroom.level==leveltype).all()
    # print spec_results

    # url_id = spec_results.class_id
    # results = []

    # for res in spec_results:
    #     results.append(res.class_id)

    results = {}

    # add matching classes to results dictionary
    for res in spec_results:
        url_id = res.class_id
        results[res.class_name] = [res.cost, res.per_time]

    if results.items():
        for name, cost_time in results.items():
            render_results = '{}: {}0/{}'.format(name, cost_time[0], cost_time[1])

        return render_template('search-results.html', render_results=render_results, name=name, cost_time=cost_time, 
                                                    results=results, spec_results=spec_results, res=res, url_id=url_id,
                                                    leveltype=leveltype, languagetype=languagetype)
    else:
        return "Sorry, we don't have that class right now"


    # NOTES FROM DOBS!!!!!
    #     form_inputs = request.form.get("form")
    # form inputs will be gargbae
    # have to do regex
    # return "WE are good"
    # return jsonify({"emotion" : "sad"})


@app.route('/class-info/<url_id>')
def class_info(url_id):
    """Renders information about a class that has been selected."""

    # Queries db for clicked on class
    returned_classes = db.session.query(Classroom).filter(Classroom.class_id==url_id).first()
    print "returned class info:"
    print returned_classes
    print returned_classes.class_name

    all_class = db.session.query(User).join(ClassUser).filter(ClassUser.class_id==url_id).all()
    # for user in all_class:
    # print all_class.user_id


    return render_template("class-info.html", returned_classes=returned_classes, url_id=url_id, all_class=all_class)


@app.route('/join-class', methods=["POST"])
def join_class():
    """Adds a user_id to a class and shows update on profile.html"""


    # gets class_id from viewed class
    id_class = request.form.get("id-class")

    # checks if user is logged in
    user_account = User.query.filter_by(user_id=session["user_id"]).first()
    user_username = user_account.username
    print user_username

    class_info = db.session.query(Classroom).filter_by(class_id=id_class).one()
    print "class_info"
    print type(class_info)
    print class_info.language

    # adds logged in user-class association to db
    if not session["user_id"]:
        flash("you need to log in")
    else:
        add_stud = ClassUser(user_id=user_account.user_id, class_id=id_class)
        print "Yeah!"

        db.session.add(add_stud)
        db.session.commit()

        print "dinosaur"
        return render_template("join-class.html", class_info=class_info, user_username=user_username)



@app.route('/create-class')
def create_class_form():
    """Take teacher input from class creation form"""
    
    return render_template('create-class.html')



@app.route('/created-results', methods=(["POST"]))
def class_submission():
    """Message that class has been created"""

    # This is where the create-class info is held as a post
    title = request.form.get("class-name")
    language = request.form.get("languagetype")
    level = request.form.get('leveltype')
    price = request.form.get('pricetype')
    min_students = request.form.get('min')
    max_students = request.form.get('max')
    days = request.form.get('days').encode('utf8')
    start_date = request.form.get('start').encode('utf8')
    end_date = request.form.get('end').encode('utf8')
    start_time = request.form.get('starttime').encode('utf8')
    end_time = request.form.get('endtime').encode('utf8')
    per_time = request.form.get('pertime')
    address = request.form.get('address')

    newclass = Classroom(language=language, level=level, min_students=min_students, 
                        max_students=max_students, class_days=days, 
                        start_date=start_date, end_date=end_date, cost=price, 
                        start_time=start_time, end_time=end_time, per_time=per_time, 
                        address=address, class_name=title) 


    db.session.add(newclass)
    db.session.commit()

    user_account = User.query.filter_by(user_id=session["user_id"]).first()
    user_username = user_account.username

    return render_template("newclass.html", language=language, level=level, 
                        min_students=min_students, max_students=max_students, class_days=days, 
                        start_date=start_date, end_date=end_date, cost=price, 
                        start_time=start_time, end_time=end_time, per_time=per_time, 
                        address=address, class_name=title, user_username=user_username)



    # form_inputs = request.form.get("form")
    # form inputs will be gargbae
    # have to do regex
    # return "WE are good"
    # return jsonify({"emotion" : "sad"})

    #return jsonify "str" jsonify { apple: 1, berry:2}



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