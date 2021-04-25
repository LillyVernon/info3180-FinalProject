"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
import jwt
from app import db, login_manager
from flask import render_template, request,  redirect, url_for, session, abort, send_from_directory,jsonify, flash,  g, make_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_car,User_fav, Users
from .forms import RegisterForm, AddCarForm, LoginForm, UploadForm
from datetime import date
from flask import _request_ctx_stack
from functools import wraps

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

@app.route('/api/upload', methods=["POST"])
def upload():
    form=UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        photo=request.files['photo']
        description=request.form['description']
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File Saved', 'success')
        print(description)
        successful={"message":"File Upload Successful", "filename":filename, "description": description}
        return jsonify(successful=successful)
    else:
        errors={"errors":form_errors(form)}
        return jsonify(errors=errors)


@app.route('/api/auth/login',  methods=['POST'])

def login():
    form=LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
        login_user(user)
        token = jwt.encode({'id':user.user_id, 'user': user.username}, app.config['SECRET_KEY'], algorithm = 'HS256')
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
    return jsonify(errors=errors) 



@app.route("/api/auth/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('login'))

@app.route("/api/cars", methods=["POST", ])
@login_required
def cars():

    form=AddCarForm()
    if request.method == 'POST' and form.validate_on_submit():

        photo=form.photo.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        desc = request.form['description']
        make = request.form['make']
        model = request.form['model']

        colour = request.form['colour']
        year = request.form['year']
        transmis = request.form['transmission']
        car_type = request.form['car_type']
        price = request.form['price']
        car=User_car(desc,make,model,colour,year,transmis, car_type, price,filename)
        #db.session.add(car)
        #db.session.commit()
        
        return 

@app.route('/api/users/<user_id>', methods=['GET'])
@requires_token
def userDetails(user_id):
    user=Users.query.get(user_id)
    reqs={'id':user.user_id, 'username':user.username, 'name':user.name, 'email':user.email, 'location':user.location, 'biography': user.biography, 'photo':user.photo, 'date_joined': user.datejoined }
    return jsonify(reqs)

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