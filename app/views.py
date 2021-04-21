"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request,  redirect, url_for, session, abort, send_from_directory,jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename,check_password_hash
from app.models import user_car,user_fav, user
###
# Routing for your application.
###
@app.route('/api/upload', methods=["POST"])
def register():
    form="ADD form class"
    User=""
    if request.method == 'POST' and form.validate_on_submit():
        photo=form.photo.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        username=request.form['username']
        password=request.form['password']
        user=User(username,password,request.form['fullname'],request.form['email'], request.form['location'], request.form['biography'],filename)
        #db.session.add(user)
        #db.session.commit()
        successful={"message":"File Upload Successful", "user":username}
        return jsonify(successful=successful)
    else:
        errors={"errors":form_errors(form)}
        return jsonify(errors=errors)

@app.route('/api/auth/login')
def login():
    form=""
    User=""
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        login_user(user)
        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

            # If the user is not blank, meaning if a user was actually found,
            # then login the user and create the user session.
            # user should be an instance of your `User` class
            login_user(user, remember=remember_me)

            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

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
    if request.method == 'GET':
            
        cars=db.session.query(user_cars).all()
        return render_template("properties.html", items=cars)
    elif request.method == 'POST' and form.validate_on_submit():

        photo=form.photo.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        desc = request.form['description']
        make = request.form['make']
        model = request.form['model']
        color = request.form['color']
        year = request.form['year']
        transmis = request.form['transmission']
        car_type = request.form['car_type']
        price = request.form['price']
        car=user_car(desc,make,model,color,year,transmis, car_type, price,filename)
        #db.session.add(car)
        #db.session.commit()
        
        return 

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

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
