"""Class Finder Flask Routes"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Classroom, User, ClassUser

import datetime

import json

import re

# import stripe
# stripe.api_key = STRIPE_PERSONAL_KEY


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

    return render_template("login.html", id_class=None)


@app.route('/login-visitor')
def login_from_classinfo():
    """Login for visitors"""

    id_class = request.args.get("id-class")
    print id_class

    return render_template("login.html", id_class=id_class)


@app.route('/login-success', methods=["POST"])
def check_login():
    """Checks info and logs user in to session"""

    email = request.form.get("email")
    password = request.form.get("password")

    user_account = User.query.filter_by(email=email, password=password).first()
    print user_account
    user_username = user_account.username
    print user_username

    if user_account:
        print user_account
        session["user_id"] = user_account.user_id
    #     print session["user_id"]
        return render_template("login-success.html", user_account=user_account, user_username=user_username, id_class=None)
    # else:
    #     flash("Wrong email or password, try again")
    #     return redirect ("/login")

    # elif email == user_account:
    #         flash("That email is invalid.")
    #         return redirect('/login')
    # elif password != user_account:
    #     flash("That password is invalid.")
    #     return redirect('/login')

@app.route('/login-success-visitor', methods=["POST"])
def check_visitor_login():
    """Checks user info and sends them to the class they were looking at"""

    email = request.form.get("email")
    password = request.form.get("password")

    id_class = request.form.get("id-class")

    user_account = User.query.filter_by(email=email, password=password).first()
    print user_account
    user_username = user_account.username
    print user_username

    print id_class

    if user_account:
        print user_account
        session["user_id"] = user_account.user_id
        print session["user_id"]
        return redirect('/class-info/'+id_class)


@app.route('/create-profile')
def create_user_profile():
    """Takes teacher and/or student input for profile info"""

    return render_template('create-profile.html')


@app.route('/new-profile', methods=["POST"])
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

        user = User(email=email, username=username, fname=fname, lname=lname, 
            password=password, is_teacher=isteacher, bio=bio)
        #white is above vars, orange is db fieldnames
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.user_id

        user_account = User.query.filter_by(email=email, password=password).first()
        user_username = user_account.username

        print "New user added"
        print session["user_id"]
        return redirect('/profile/' + user_username)

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


    return render_template("profile.html", user_email=user_email, user_classes=user_classes, user_username=user_username)


@app.route('/logout')
def logout():
    """Logout button and session end"""

    session.clear()

    return redirect('/')


@app.route('/search')
def search_classes():
    """Search Box and browsing/parameters"""

    if session:
        user_email = db.session.query(User).filter(User.user_id == session["user_id"]).first()
        user_username = user_email.username

        return render_template('search.html', user_username=user_username)

    return render_template('search.html', user_username=None)



@app.route('/search-results', methods=["GET"])
def search_by_lang():
    """Search Results for Language and Level"""

    # Gets language input from dropdown in search.html
    languagetype = request.args.get("languagetype")
    leveltype = request.args.get("leveltype")
    # print languagetype

    # lang_result = db.session.query(Classroom.class_id, Classroom.language).all()


    # gives me a list of objects
    parameter_results = db.session.query(Classroom).filter(Classroom.language==languagetype, Classroom.level==leveltype).all()

    results = {}

    # add matching classes to results dictionary
    for res in parameter_results:
        results[res.class_name] = [res.cost, res.per_time, res.class_id]

    if results.items():
        for name, cost_time in results.items():
            # render_results = '{}: {}/{}, {}'.format(name, cost_time[0], cost_time[1], cost_time[2])

                return render_template('search-results.html', name=name, cost_time=cost_time, results=results, 
                                                            parameter_results=parameter_results, res=res, leveltype=leveltype, 
                                                            languagetype=languagetype, url_id=res.class_id)
    else:
        return "Sorry, we don't have that class right now"


        # NOTES FROM DOBS!!!!!
        #     form_inputs = request.form.get("form")
        # form inputs will be gargbae
        # have to do regex
        # return "WE are good"
        # return jsonify({"emotion" : "sad"})



@app.route('/map.json', methods=["GET"])
def search_reults_ajax():
    """renders map on class-info page"""

    class_id = request.args.get("class_id")

    returned_classes = db.session.query(Classroom).filter(Classroom.class_id==class_id).first()
    address=returned_classes.address

    print address
    return address



@app.route('/class-info/<int:url_id>')
def class_info(url_id):
    """Renders information about a class that has been selected."""

    # Queries db for clicked on class
    returned_classes = db.session.query(Classroom).filter(Classroom.class_id==url_id).first()
    print "returned class info:"
    print returned_classes
    print returned_classes.class_name
    print returned_classes.address
    print returned_classes.class_id

    all_class = db.session.query(User).join(ClassUser).filter(ClassUser.class_id==url_id).all()
    address=returned_classes.address

    if session.get("user_id"):

        logged_in = User.query.filter(User.user_id==session["user_id"]).first()
        print "look here: ", logged_in.is_teacher

        if logged_in.is_teacher == 0:
            print "if student, class: "
            print returned_classes.class_id

            return render_template("class-info.html", returned_classes=returned_classes, url_id=url_id, 
                                                    all_class=all_class, logged_in=logged_in)

        else:
            print "if teacher, class: ", returned_classes.class_id
            return render_template("class-info-teacher.html", returned_classes=returned_classes, url_id=url_id, 
                                                            all_class=all_class, logged_in=logged_in)


    return render_template("class-info.html", returned_classes=returned_classes, url_id=url_id, 
                                                            all_class=all_class, logged_in=None)




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
        the_class = ClassUser.query.filter(ClassUser.class_id==id_class).first()
        add_stud = ClassUser(user_id=user_account.user_id, class_id=id_class)

        # adds user to class in db
        if add_stud.user_id != the_class.user_id:
            db.session.add(add_stud)
            db.session.commit()

            # updates c_count in db
            update_count = class_info.c_count + 1

            db.session.query(Classroom).filter(Classroom.class_id == id_class).update({Classroom.c_count: update_count})
            db.session.commit()


            return render_template("join-class.html", class_info=class_info, user_username=user_username)
        else:
            return "You're already in that class!"



@app.route('/dropped', methods=["POST"])
def drop_class():
    """Removes student from that class in the db"""


    # Class ID being dropped
    id_class = request.form.get("id-class")
    print "id_class", id_class

    # db query for class-user association
    the_class = ClassUser.query.filter(ClassUser.class_id==id_class, ClassUser.user_id==session['user_id']).first()


    # deletes association and removes class info from user profile page
    db.session.delete(the_class)
    db.session.commit()


    # to pass username in the url
    name = User.query.filter_by(user_id=session["user_id"]).first()
    user_username = name.username
    url = '/profile/' + str(user_username)

    return redirect(url)



@app.route('/enrolled-in/<url_id>')
def enrolled_in(url_id):
    """Renders information about a class that the student is in."""

    user_info = User.query.filter_by(user_id=session["user_id"]).first()
    print "user id: "
    print user_info.user_id


    # Queries db for clicked on class
    returned_classes = db.session.query(Classroom).filter(Classroom.class_id==url_id).first()
    print "returned class info:"
    print returned_classes
    print returned_classes.class_name

    all_class = db.session.query(User).join(ClassUser).filter(ClassUser.class_id==url_id).all()
    print all_class


    return render_template("enrolled-in.html", returned_classes=returned_classes, url_id=url_id, 
                                                all_class=all_class, user_info=user_info)


@app.route('/enrolled.json', methods=["POST"])
def process_rating():

    ratings = float(request.form.get("rating"))
    class_rate = float(request.form.get("classid"))
    print "class_rate: ", type(class_rate), class_rate
    print "ratings: ", type(ratings), ratings

    class_to_rate = Classroom.query.filter(Classroom.class_id==class_rate).first()
    class_to_rate.rating_count = float(class_to_rate.rating_count)
    print class_to_rate.rating_count

    rating_update = (class_to_rate.rating*class_to_rate.rating_count+ratings)/(class_to_rate.rating_count+1)
    up_count = Classroom.rating_count + 1

    db.session.query(Classroom).filter(Classroom.class_id==class_rate).update({Classroom.rating_count: Classroom.rating_count+1})
    db.session.commit()
    print "class_to_rate, rating_count", class_to_rate.rating_count
    db.session.query(Classroom).filter(Classroom.class_id==class_rate).update({Classroom.rating: rating_update})
    db.session.commit()

    print "class_to_rate, rating: ", class_to_rate.rating
    print "OMG, it worked!!!"
    return "Thanks for rating this class!"



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
    start_time = request.form.get('starttime')
    end_time = request.form.get('endtime')
    per_time = request.form.get('pertime')
    address = request.form.get('address')
    c_count = request.form.get("c-count")
    first_rate = request.form.get("first-rate")
    r_count = request.form.get("r-count")


    # convert start_date and end_date to datetime objects with strptime()
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    print start
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print end
    time_start = datetime.datetime.strptime(start_time, '%H:%M')
    print time_start
    time_end = datetime.datetime.strptime(end_time, '%H:%M')
    print time_end

    now = datetime.datetime.now()
    print now

    # REGEX FOR CHECKBOXES!!!
    # test = Classroom.query.filter_by(class_id=4).first()

    # time = str(test.per_time)
    # print time

    # REGEX for class days, calls it days_class
    day_join = str(days)
    day_join = re.sub('&',', ', day_join)
    days_split = re.sub('days=', '', day_join)
    print "DAYS_SPLIT: ", days_split

    # dino = str(test.class_days)
    # dino = re.sub('&',', ', dino)
    # dino_thing = re.sub('days=', '', dino)

    # Counts number of days/week of class, calls it: counter
    counter = 0
    for day in days_split.split(' '):
        counter = counter + 1
    print "COUNTER: ", counter

    # Finds duration of each class, calls it
    a = datetime.datetime.strptime(start_time, '%H:%M') 
    print "A: ", a, type(a)
    b = datetime.datetime.strptime(end_time, '%H:%M')
    print "B: ", b, type(b)

    difference = b - a

    hours = difference.seconds//3600
    minutes = difference.seconds//60 % 60
    duration = ((hours*60.0) + minutes)/60.0
    print "DURATION: ", duration

    # Base price based on per hour, calls it b_price
    time = str(per_time)
    print "PER_TIME: ", type(time)
    print "PRICE: ", type(price)
    price = float(price)

    if time == 'hour':
        base_price = price
    elif time == 'week':
        base_price = price/(counter*duration)
    elif time == 'month':
        base_price = price/(counter*duration*4.3)
    elif time == 'year':
        base_price = price/(counter*duration*52)

    print "BASE_PRICE: ", base_price


    newclass = Classroom(language=language, level=level, min_students=min_students, 
                        max_students=max_students, class_days=days, 
                        start_date=start, end_date=end, cost=price, 
                        start_time=time_start, end_time=time_end, per_time=per_time, 
                        address=address, class_name=title, c_count=c_count, create_date=now,
                        rating_count=r_count, rating=first_rate, base_price=base_price) 

    print newclass


    db.session.add(newclass)
    db.session.commit()

    user_account = User.query.filter_by(user_id=session["user_id"]).first()
    user_username = user_account.username

    add_teach = ClassUser(user_id=user_account.user_id, class_id=newclass.class_id)

    db.session.add(add_teach)
    db.session.commit()

    return "You have successfully created this class!"

    # return render_template("newclass.html", language=language, level=level, 
    #                     min_students=min_students, max_students=max_students, class_days=days, 
    #                     start_date=start_date, end_date=end_date, cost=price, 
    #                     start_time=start_time, end_time=end_time, per_time=per_time, 
    #                     address=address, class_name=title, user_username=user_username)



    # return jsonify({"emotion" : "sad"})

    #return jsonify "str" jsonify { apple: 1, berry:2}



# @app.route('/teacher')


@app.route('/test')
def test_map():
    """This is a testing route"""

    # returned_classes = db.session.query(Classroom).filter(Classroom.class_id==url_id).first()
    # print "returned class info:"
    # print returned_classes
    # print returned_classes.class_name

    # all_class = db.session.query(User).join(ClassUser).filter(ClassUser.class_id=="10").all()
    # for user in all_class:
    # print all_class.user_id



    # print "START TIME: ", test.start_time
    # print type(test.start_time)
    # print "END TIME: ", test.end_time
    # print type(test.end_time)


    # a = datetime.datetime.now()
    # >>> b = datetime.datetime.now()
    # >>> c = b - a
    # datetime.timedelta(0, 8, 562000)
    # >>> divmod(c.days * 86400 + c.seconds, 60)
    # (0, 8)


    return "womp womp"


    # FOR DAYS???

    #     test = Classroom.query.filter_by(class_id=2).first()
    # days = str(test)
    # days = re.sub('&',', ', days)
    # days_class = re.sub('days=', '', days)
    # print "DAYS_CLASS: ", days_class

    # counter = 0
    # for day in days_class.split(' '):
    #     counter = counter + 1
    #     print "COUNTER: ", counter

    #     return "Hello"

    # User.query.filter_by(user_id=session["user_id"]).first()

    # return render_template('test.html', all_class=all_class)
    # return render_template('class-info-teacher.html')


@app.route('/ajax-love.json', methods=["POST"])
def ajax_practice():
    """I'm going to learn this!"""

    ratings = request.form.get("rating")



    print "OMG, it worked!!!"
    return "Thanks for rating this class?"


@app.route('/ajax-ajax')
def more_ajax_html():
    """for reals"""


    return render_template("loving-the-ajax.html")






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()