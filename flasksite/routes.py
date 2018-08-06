import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flasksite import app, db, bcrypt
from flasksite.forms import RegistrationForm, LoginForm, UpdateAccountForm, Top10Form
from flasksite.models import User, Post, Selection, Event
from flasksite.scrape import entries_list
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'David Turner',
        'title': 'Blog post one',
        'content': 'This is the first blog post',
        'date_posted': '1st August 2018'
    },
    {
        'author': 'Sarah Turner',
        'title': 'Blog post two',
        'content': 'This is the second blog post',
        'date_posted': '2nd August 2018'
    },
    {
        'author': 'David Turner',
        'title': 'Blog post three',
        'content': 'This is the third blog post',
        'date_posted': '3nd August 2018'
    }
]
# Reverse the array to show the last item first.
posts = posts[::-1]


@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        pic = url_for('static', filename='profile_pics/' + current_user.image_file)
        return dict(pic=pic)
    else:
        pic = None
        return dict(pic=pic)



@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in!',
              'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
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
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/tips", methods=['GET', 'POST'])
@login_required
def tips():
    form = Top10Form()
    active_event = Event.query.filter_by(active=True).first()
    active_event = active_event.full_name + ' ' + active_event.year
    if form.validate_on_submit():
        selection = Selection(
                    user_id=current_user.id,
                    event_id=1,  # Germany. Get the event id from whether event is active or not.
                    top10_selection_1=form.position_1.data,
                    top10_selection_2=form.position_2.data,
                    top10_selection_3=form.position_3.data,
                    top10_selection_4=form.position_4.data,
                    top10_selection_5=form.position_5.data,
                    top10_selection_6=form.position_6.data,
                    top10_selection_7=form.position_7.data,
                    top10_selection_8=form.position_8.data,
                    top10_selection_9=form.position_9.data,
                    top10_selection_10=form.position_10.data,
                    stage_two_selection=form.stage_two_selection.data,
                    power_stage_selection=form.power_stage_selection.data)
        db.session.add(selection)
        db.session.commit()
        flash('Your selections have been updated.', 'success')
        return redirect(url_for('tips'))
    elif request.method == 'GET':
        if Selection.query.filter_by(user_id=current_user.id). \
                                filter_by(event_id=1).order_by('-id').first():

            autofill = Selection.query.filter_by(user_id=current_user.id). \
                                    filter_by(event_id=1).order_by('-id').first()

            form.position_1.data = autofill.top10_selection_1
            form.position_2.data = autofill.top10_selection_2
            form.position_3.data = autofill.top10_selection_3
            form.position_4.data = autofill.top10_selection_4
            form.position_5.data = autofill.top10_selection_5
            form.position_6.data = autofill.top10_selection_6
            form.position_7.data = autofill.top10_selection_7
            form.position_8.data = autofill.top10_selection_8
            form.position_9.data = autofill.top10_selection_9
            form.position_10.data = autofill.top10_selection_10
            form.stage_two_selection.data = autofill.stage_two_selection
            form.power_stage_selection.data = autofill.power_stage_selection
    return render_template('tips.html', title='Tips', form=form, entries_list=entries_list, active_event=active_event)
