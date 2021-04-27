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
###
# Routing for your application.
###
@app.route('/api/secure', methods=['GET'])
@requires_token
def api_secure():
    # This data was retrieved from the payload of the JSON Web Token
    # take a look at the requires_auth decorator code to see how we decoded
    # the information from the JWT.
    user = g.current_user
    return jsonify(data={"user": user}, message="Success")

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

@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            user = Users.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                payload = { 'username': user.username,'userid': user.user_id}
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                session['userid'] = user.user_id
                success=jsonify(message="Logged in Successfully",data={"token":token})         
                return success
            else: 
                return jsonify(message="Login Failed") 
        else:
            error=form_errors(form)
            jsonErr=jsonify(errors=error)
            return jsonErr

@app.route('/api/auth/logout', methods=['POST'])
@requires_token
def logout():
    user = g.current_user
    return jsonify(data={"user": user}, message="You were logged out")



@app.route('/api/register', methods=['POST'])
def register():
    form=RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
    
            photo=request.files['photo'] 
            filename=secure_filename(photo.filename)
            datejoined=date.today()
            user=Users(request.form['username'],request.form['password'],request.form['fullname'], request.form['email'], request.form['location'], request.form['biography'],
            filename,datejoined)
            if user is not None:
                db.session.add(user)
                db.session.commit()
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                successful={'message': 'You are now registered',}  
                return jsonify(successful=successful)
        else:
            errors={"errors":form_errors(form)}
            return jsonify(errors=errors)


@app.route('/api/cars', methods=['POST','GET'])
@requires_token
def car():
    form=AddCarForm()
    if request.method == 'POST':
       
        if form.validate_on_submit():

            photo=form.photo.data
            filename=secure_filename(photo.filename)
            car=User_car(form.description.data,form.make.data,form.model.data,form.colour.data, form.year.data, form.transmission.data,form.car_type.data,form.price.data,
            filename,g.current_user["userid"])
            #car=User_car(make=form.make.data,model=model,colour=colour, year=year, transmis=trans,car_type=cartype,price=price,desc=desc,photo=filename,user_id=g.current_user["userid"])
            #car=Cars(description=desc, make=make, model=model, colour=colour, year=year, transmission=trans, car_type=cartype, price=price, photo=pic, user_id=current_user.user_id )
            if car is not None:
                db.session.add(car)
                db.session.commit()
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                success={'message': 'Car Registered Successfully'}  
                return jsonify(success=success)
        else:
            return jsonify(errors=form_errors(form))
            
    if request.method == 'GET':
        usercars=[]
        getcars=User_car.query.order_by(User_car.car_id).all()
        for car in getcars:
            car={'id':car.car_id,"user_id":car.user_id,"year":car.year, "price":car.price,"photo":car.photo,"make":car.make,"model":car.model, }
            usercars.append(car)
        return jsonify(allcars=usercars)
        
@app.route('/api/cars/<car_id>', methods=['GET'])
@requires_token
def car_details(car_id):       
    if request.method == 'GET':
        f=False
        car=User_car.query.filter_by(car_id=car_id).first()
        favs=User_fav.query.filter((User_fav.car_id==car_id) and (User_fav.user_id==g.current_user["userid"])).first()
        if favs!=None:
            f=True
        return jsonify(car_id=car.car_id,model=car.model,make=car.make,user_id=car.user_id,car_type=car.car_type,
            desc=car.desc,price=car.price,photo=car.photo,
            transmission=car.transmis,colour=car.colour,year=car.year,Favorite=f)
        
@app.route('/api/cars/<car_id>/favourite', methods=['POST'])
@requires_token
def favourite_car(car_id):       
    if request.method == 'POST':
        userid=g.current_user['userid']
        fav=User_fav(car_id,userid)
        db.session.add(fav)
        db.session.commit()
        return jsonify(message="Car Favourited")
    
@app.route('/api/users/<user_id>', methods=['GET'])
@requires_token
def user_details(user_id):       
    if request.method == 'GET':
        userdetail=Users.query.filter_by(user_id=user_id).first()
        date_time=userdetail.datejoined
        user={'id':userdetail.user_id, 'username':userdetail.username,'name':userdetail.name,'email':userdetail.email,"location":userdetail.location,"biography":userdetail.biography,       
        "photo":userdetail.photo,
        "date_joined":date_time.strftime("%B %d, %Y")
        }
        return jsonify(user=user)

@app.route('/api/users/<user_id>/favourites', methods=['GET'])
@requires_token
def user_favourites(user_id): 
    favcars=[]      
    if request.method == 'GET':
        favorite=User_fav.query.filter_by(user_id=user_id).all()
        for fave in favorite:
            cardetail=User_car.query.filter_by(car_id=fave.car_id).first()
            car={'id':cardetail.car_id, "user_id":cardetail.user_id,"year":cardetail.year,"price":cardetail.price,"photo":cardetail.photo,"make":cardetail.make,"model":cardetail.model}
            favcars.append(car)
        return jsonify(favouritecars=favcars)
               


@app.route('/api/search',methods=["GET"])
@requires_token
def car_search():
    search=[]
    if request.method=="GET":
        make=request.args.get('searchbymake')
        model=request.args.get('searchbymodel')
        cars= User_car.query.filter((User_car.make.like(make) or User_car.model.like(model)))
        for car in cars:
            car={'id':car.car_id,"user_id":car.user_id,"year":car.year,"price":car.price,"photo":car.photo,"make":car.make,"model":car.model}
        search.append(car)
        return jsonify(searchedcars=search)
            

        
        
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
        



###
# The functions below should be applicable to all Flask apps.
###

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

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
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