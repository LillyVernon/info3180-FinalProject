"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os,base64,datetime
from app import app
import jwt
from app import db, login_manager
from flask import render_template, request,  redirect, url_for, session, abort, send_from_directory,jsonify, flash,  g, make_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_car,User_fav, Users
from .forms import RegisterForm, AddCarForm, LoginForm, Search
from datetime import date
from flask import _request_ctx_stack
from functools import wraps
from app.config import *

def requires_token(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


@app.route('/api/secure', methods=['GET'])
@requires_token
def api_secure():
    # This data was retrieved from the payload of the JSON Web Token
    # take a look at the requires_auth decorator code to see how we decoded
    # the information from the JWT.
    user = g.current_user
    return jsonify(data={"user": user}, message="Success")
###
# Routing for your application.
###
@app.route('/api/register', methods=['POST'])
def register():
    form=RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        photo=form.photo.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        username=request.form['username']
        password=request.form['password']
        user=Users(username,password,request.form['fullname'],request.form['email'], request.form['location'], request.form['biography'],filename,date.today())
        db.session.add(user)
        db.session.commit()
        successful={"message":"Registration Successful", "user":request.form['fullname']}
        return jsonify(successful=successful)
    else:
        errors={"errors":form_errors(form)}
        print(errors)
        return jsonify(errors=errors)



""" @app.route('/api/auth/login',  methods=['POST'])

def login():
    form=LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
        login_user(user)
        token = jwt.encode({'id':user.user_id, 'user': user.username}, app.config['SECRET_KEY'], algorithm = 'HS256').decode('utf-8')
        print(token)
        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True
            login_user(user, remember=remember_me)

            flash('Logged in successfully.', 'success')
            successful={"message":"Login Successful", "token":token}
            return jsonify(successful=successful),200
        else:
            error='Username or Password is incorrect.'
            return jsonify(error=error),400

    errors= form_errors(form)
    return jsonify(errors=errors)  """


@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            user = Users.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                payload = { 'username': user.username,'user_id': user.user_id}
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                session['user_id'] = user.user_id
                jsonmsg=jsonify(message=" Login Successful and Token was Generated",data={"token":token})         
                return jsonmsg 
            else: 
                return jsonify(message="Login Failed") 
        else:
            err=form_errors(form)
            jsonErr=jsonify(errors=err)
            return jsonErr

@app.route("/api/auth/logout", methods=["GET"])
@requires_token
def logout():
    # Logout the user and end the session
    logout_user()
    user = g.current_user
    response = "You were logged out successfully."
    return jsonify(data={"user": user}, message="Logged Out")

''' @app.route("/api/cars", methods=["POST","GET"])
@login_required
def cars():
    response=''
    form=AddCarForm()
    if request.method == 'POST' :
        if form.validate_on_submit():
            photo=form.photo.data
            filename=secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            desc = request.form['description']
            make = request.form['make']
            model = request.form['model']
            colour = request.form['colour']
            year = request.form['year']
            transmis =form.transmission.data
            user_id = g.current_user["user_id"]
            car_type = form.car_type.data
            price = request.form['price']

            car=User_car(desc,make,model,colour,year,transmis, car_type, price,user_id,filename)
            db.session.add(car)
            db.session.commit()
            #successful={"message":"Registration Successful"}
            response="Car Added"
            #return jsonify(successful=successful),200
            return jsonify(message=response),201
        else:
            errors={"errors":form_errors(form)}
            return jsonify(errors=errors),400 '''

@app.route('/api/cars', methods=['POST','GET'])
@requires_token
def car():
    # Instantiate your form class
    form=AddCarForm()
    # Validate file upload on submit
    
    if request.method == 'POST':
        print(request.form['description'])
        print(request.form['transmission'])
        if form.validate_on_submit():
        # Get file data and save to your uploads folder
            make=request.form['make']
            model=request.form['model']
            colour=request.form['colour']
            year=request.form['year']
            price=request.form['price']
            cartype=request.form['car_type']
            print(cartype)
            trans=request.form['transmission']
            print(trans)
            desc=request.form['description']
            print(desc)
            pic=request.files['photo'] # or form.pic.data
            filename=secure_filename(pic.filename)
            car=User_car(make=make,model=model,colour=colour, year=year, transmis=trans,car_type=cartype,price=price,desc=desc,photo=filename,user_id=g.current_user["user_id"])
            #car=Cars(description=desc, make=make, model=model, colour=colour, year=year, transmission=trans, car_type=cartype, price=price, photo=pic, user_id=current_user.user_id )
            if car is not None:
                db.session.add(car)
                db.session.commit()
                pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                jsonmsg={'message': 'Car added Successful'}  
                return jsonify(jsonmsg=jsonmsg)
        else:
            return jsonify(errors=form_errors(form))
            
    if request.method == 'GET':
        allc=[]
        cars=User_car.query.order_by(User_car.car_id).all()
        for c in cars:
            car={}
            car['id']=c.car_id
            car["user_id"]=c.user_id
            car["year"]=c.year        
            car["price"]=c.price
            car["photo"]=c.photo
            car["make"]=c.make
            car["model"]=c.model
            allc.append(car)
        return jsonify(allcars=allc)
        
''' @app.route('/api/users/<user_id>', methods=['GET'])
@requires_token
def userDetails(user_id):
    #user=Users.query.get(user_id)
    user=Users.query.filter_by(user_id=user_id).first()
    reqs={'id':user.user_id, 'username':user.username, 'name':user.name, 'email':user.email, 'location':user.location, 'biography': user.biography, 'photo':user.photo, 'date_joined': user.datejoined }
    print(reqs)
    return jsonify(reqs) '''

@app.route('/api/users/<user_id>', methods=['GET'])
@requires_token
def user_details(user_id):       
    if request.method == 'GET':
        print(g.current_user["user_id"])
        userdetail=Users.query.filter_by(user_id=g.current_user["user_id"]).first()
        date_time=userdetail.datejoined
        user={'id':userdetail.user_id, 'username':userdetail.username,'name':userdetail.name,'email':userdetail.email,"location":userdetail.location,"biography":userdetail.biography,       
        "photo":userdetail.photo,
        "date_joined":date_time.strftime("%B %d, %Y")
        }
        return jsonify(user=user)

''' @app.route('/api/search', methods =["GET"])
@requires_token
def search():
    form = Search()
    result=[]
    if request.method=="GET":
        model=request.form["model"]
        make =request.form["make"]
        if model == '' and make == '':
            cars=db.session.query(User_car).all()
        elif model == '':
            cars=db.session.query(User_car).filter_by(make=make).all()
        elif make == '':
            cars=db.session.query(User_car).filter_by(model=model).all()
        #else:
            #cars=db.session.query(User_car).order_by(car_id).limit(3).all()[::-1]
        
        for car in cars:
            car ={
                "id": car.car_id,
                    "description": car.desc,
                    "year": car.year,
                    "make": car.make,
                    "model": car.model,
                    "colour": car.colour,
                    "transmission": car.transmis,
                    "cartype": car.car_type,
                    "price": car.price,
                    "photo": car.photo,
                    
                    }
            result.append(car)
        return jsonify(search=result)
    else:
        response = {"errors": form_errors(form)}
        return  jsonify(response) '''

@app.route('/api/search',methods=["GET"])
@requires_token
def search():
    result=[]
    if request.method=="GET":
        make=request.args.get('searchmake')
        model=request.args.get('searchmodel')
        cars= User_car.query.filter((User_car.make.like(make)|User_car.model.like(model)))
        for car in cars:
            car={
           'id':car.car_id,
            "user_id":car.user_id,
            "year":car.year  ,          
            "price":car.price,
            "photo":car.photo,
            "make":car.make,
            "model":car.model}
            search.append(car)
        return jsonify(cars=result)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
            
@login_manager.user_loader
def load_user(user_id):
    return Users.get_id(user_id)
# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".
    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")