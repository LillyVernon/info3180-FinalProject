from . import db
from werkzeug.security import generate_password_hash

class Users(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    location = db.Column(db.String(255))
    biography= db.Column(db.String(255))
    photo= db.Column(db.String(255))
    datejoined = db.Column(db.DateTime)

    def __init__(self, username, password, name,email, location, biography, photo, datejoined):
        self.username =username
        self.name = name
        self.email = email
        self.password=generate_password_hash(password, method='pbkdf2:sha256')
        self.location=location
        self.biography=biography
        self.photo=photo
        self.datejoined=datejoined

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Users %r>' % (self.username)


class User_car(db.Model):
    
    __tablename__ = 'user_car'

    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(255))
    make = db.Column(db.String(80))
    model = db.Column(db.String(29))
    colour = db.Column(db.String(225))
    year = db.Column(db.String(225))
    transmis = db.Column(db.String(225))
    car_type = db.Column(db.String(225))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer)
    photo=db.Column(db.String(225))   

    def __init__(self, desc, make, model, colour, year, transmis, car_type, price,  photo):
        self.desc = desc
        self.make = make
        self.model = model
        self.colour = colour
        self.year = year
        self.transmis = transmis
        self.car_type = car_type
        self.price=price
        self.photo=photo

 
    
class User_fav(db.Model):
     __tablename__ = 'user_fav'

     user_favid = db.Column(db.Integer, primary_key=True, autoincrement=True)
     car_id=db.Column(db.Integer)
     user_id = db.Column(db.Integer)


