"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import Classroom
from model import User
from model import ClassUser

from model import connect_to_db, db
from server import app


def load_classes():
    """Load classes from class.txt into database"""

    print "Classes"

    # Deletes all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Classroom.query.delete()

    # Read class.txt file and insert data
    for row in open("seed_data/class.txt"):
        row = row.rstrip()
        class_id, language, level, cost, min_students, max_students, latitude, longitude, class_days, start_date, end_date, time = row.split("|")
        print "class_id: {}, language: {}, level: {}".format(class_id, language, level)

        classes = Classroom(class_id=class_id, language=language,
                        level=level, cost=cost,
                        min_students=min_students, max_students=max_students,
                        latitude=latitude, longitude=longitude,
                        class_days=class_days, start_date=start_date,
                        end_date=end_date, time=time)

        # Needs to be added to the session or it won't be stored
        db.session.add(classes)

    # Once finished, needs to be committed
    db.session.commit()

def load_users():
    """Load users from user.txt into database"""

    print "Users"


    User.query.delete()

    for row in open("seed_data/user.txt"):
        row = row.rstrip()
        user_id, username, email, password, fname, lname, is_teacher, image, bio = row.split("|")
        print "user_id: {}, f_name: {}, is_teacher: {}".format(user_id, f_name, is_teacher)

        user = User(user_id=user_id, username=username,
                    email=email, password=password,
                    fname=fname, lname=lname,
                    is_teacher=is_teacher, image=image,
                    bio=bio)

        db.session.add(user)

    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_classes()
    load_users()