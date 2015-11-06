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

@app.route('/login-success', methods=["POST"])
def check_login():
    """Checks info and logs user in to session"""

    # Flask Post

    email = request.form.get("email")
    password = request.form.get("password")

    # all_users = User.query.all()
    # print all_users

    user_account = User.query.filter(User.email == email, User.password == password).first()
    print user_account

    # print "user_account.email:" + user_account.email

    if user_account:
        print user_account
        session["user-email"] = email
        # flash("You're logged in now!")
        print session["user-email"]
        # url = '/profile/' + str(user_account.user_id)
        # return redirect(url)
        return render_template("profile.html")
    else:
        flash("Wrong email or password, try again")
        return redirect ("/login")

    # elif email == user_account:
    #         flash("That email is invalid.")
    #         return redirect('/login')
    # elif password != user_account:
    #     flash("That password is invalid.")
    #     return redirect('/login')


    # return render_template("/profile")



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
    """Search Box and browsing/parameters"""
    # selectedlanguage = use the get for languagetype() 
    # languages = db.session(Classroom).filter(Classroom.language==selectedlang).all()
    # for language in languages:
    # level = language.level

    return render_template('search.html')


@app.route('/search-results', methods=["GET"])
def search_by_lang():
    """Search Results for Language and Level"""

    # Gets language input from dropdown in search.html
    languagetype = request.args.get("languagetype")
    print languagetype

    lang_result  = db.session.query(Classroom.class_id, Classroom.language).all()

    # enough for search box
    for lang in lang_result :
        for tup in lang:
            if tup == languagetype:
                print lang

    # Gets level input from dropdown and returns classes by level
    leveltype = request.args.get("leveltype")
    print leveltype

    level_result  = db.session.query(Classroom.class_id, Classroom.level).all()
    # print level_result

    # enough for search box
    for lev in level_result:
        for thing in lev:
            if thing == leveltype:
                print lev
    # else:
    #     print "Sorry, that doesn't exist right now"

        # let's improve this to check that the glass and the level coincide and not show repeats
        # the else statement can be separated, to avoid reprinting repeatedly
        # The search box can be for if you want to only search for one parameter

    # print lev
    # print lang

    # if lev[0] == lang[0]:
    #     print "Rar"

    # return render_template('search-results.html')


    # NOTES FROM DOBS!!!!!
    #     form_inputs = request.form.get("form")
    # form inputs will be gargbae
    # have to do regex
    # return "WE are good"
    # return jsonify({"emotion" : "sad"})







@app.route('/class-info')
def class_info():
    """Reveals information about a class. Such as: language, level, days, times, teacher, students"""

    all_classes = db.session.query(Classroom).first()

    # firstday = all_classes.start_date.strftime(%B, %-d, %Y)

    
    return render_template("class-info.html", all_classes=all_classes)


@app.route('/create-class')
def create_class_form():
    """Take teacher input from class creation form"""
    
    return render_template('create-class.html')


@app.route('/created.json', methods=(["POST"]))
def class_submission():
    """Message that class has been created"""

    # This is where the create-class info is held as a post
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

    print "Monster!"

    # newclass = Classroom(language=language, level=level, min_students=min_students, 
    #                     max_students=max_students, class_days=days, 
    #                     start_date=start_date, end_date=end_date, cost=price, 
    #                     start_time=start_time, end_time=end_time, per_time=per_time, 
    #                     address=address) 


    # db.session.add(newclass)
    # db.session.commit()

    # return render_template("newclass.html", language=language, level=level, min_students=min_students, 
    #                     max_students=max_students, class_days=days, start_date=start_date, 
    #                     end_date=end_date, start_time=start_time, end_time=end_time,
    #                     address=address)


        # NOTES FROM DOBS!!!!!
    # form_inputs = request.form.get("form")
    # form inputs will be gargbae
    # have to do regex
    # return "WE are good"
    # return jsonify({"emotion" : "sad"})



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