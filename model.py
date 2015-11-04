"""Models and database functions for Class Finder"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Classroom(db.Model):
    """Classes table"""

    __tablename__ = "classes"

    class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    language = db.Column(db.String(40), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=True)
    min_students = db.Column(db.Integer, nullable=False)
    max_students = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=True)
    class_days = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=True)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    per_time = db.Column(db.String, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Class class_id={} language={}>".format(self.class_id, self.language)



class User(db.Model):
    """Users include teachers and students"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    fname = db.Column(db.String(60))
    lname = db.Column(db.String(100))
    is_teacher = db.Column(db.Boolean, nullable=False)
    image = db.Column(db.String(150))
    bio = db.Column(db.String(300))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id, self.email)



class ClassUser(db.Model):
    """Relationship table for User to the Class"""

    __tablename__ = "class_user"


    class_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=True)

    class_info = db.relationship('Classroom', backref=db.backref('class_user'))
    user_info = db.relationship('User', backref=db.backref('class_user'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Relationship user_id={} class_id={}>".format(self.user_id, self.class_id)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classfinder.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."



    # 'postgresql://localhost/classfinder'