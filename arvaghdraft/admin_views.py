from arvaghdraft import app, db, bcrypt
import os
from flask import render_template, request, session, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets

from arvaghdraft.forms import RegistrationForm, LoginForm, UpdateAccountForm
from arvaghdraft.models import Users

@app.route('/registration', methods=['GET', 'POST'])
# @login_required
def registration():
    # prevent user accessing register form if already logged in
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # else:
    # want to create new administrators so ignore top lines
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}.", 'success')
        # login in view below sends newly registered user to home page so this redundant
        return redirect (url_for('login'))
    else:
        flash(f"Wrong data entered. Please retry!", 'danger')
    return render_template('admin/registration.html', title='Register', form=form)
        
    
# login function (more secure using login_manager)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f"{form.email.data}. You have logged in successfully!", 'success')  
                # if it exists get the next page
                next_page = request.args.get('next')
                # go to login_required page page that does not require login
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash("Login Unsuccessful! Please check email and password! Also note only administrators can sign in.", 'danger')  
        return render_template('admin/login.html', title='Login', form=form)

# logout user 
@app.route('/logout')
def logout():
    logout_user()
    flash("Logout Successful!", 'success')  
    return redirect (url_for('index')) 


# get and edit the profile page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'{form.username.data} Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # populate form with existing username and email
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
    
def save_picture(form_picture):
    # ensure filenames are always different 
    random_hex = secrets.token_hex(8)
    # f_name, f_ext = os.path.splitext(form_picture.filename)
    # not using f_name above so substitute with _
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    # resize image and save (i is the newly created smaller image)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn