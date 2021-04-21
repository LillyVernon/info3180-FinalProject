from . import db
from werkzeug.security import generate_password_hash


class user_car(db.Model):
    
    __tablename__ = 'user_car'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(255))
    make = db.Column(db.String(80))
    model = db.Column(db.String(29))
    colour = db.Column(db.String(225))
    year = db.Column(db.String(225))
    transmis = db.Column(db.String(225))
    car_type = db.Column(db.String(225))
    price = db.Column(db.Decimal(225))
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

 
    
class user_fav(db.Model):
     __tablename__ = 'user_fav'

     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     car_id=db.Column(db.Integer)
     user_id = db.Column(db.Integer)


class user(db.Model):
    __tablename__ = 'user'
     
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(80))
    name= db.Column(db.String(29))
    email = db.Column(db.String(225))
    location = db.Column(db.String(225))
    biography = db.Column(db.String(225))
    photo = db.Column(db.String(225))
    date_joined=db.Column(db.DateTime)

    def __init__(self, username,  password, name, email, location, biography, photo, date_joined):
         self.username = username
         self.password = generate_password_hash(password, method='pbkdf2:sha256')
         self.name = name
         self.email = email
         self.location = location
         self.biography = biography
         self.photo=photo
         self.date_joined=date_joined


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
        return '<User %r>' % (self.username)