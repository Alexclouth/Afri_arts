from flask import render_template, url_for, flash, redirect, request, Blueprint
from web_flask import app, bcrypt, db
from web_flask.users.forms import Signup, Signin, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from web_flask.models import User, Artwork
from web_flask.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/signup", methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Signup()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password,
                    is_artist=form.is_artist.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    city=form.city.data,
                    country=form.country.data,
                    bio=form.bio.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to Login', 'success')
        return redirect(url_for('users.signin'))
    return render_template('signup.html', form=form)


@users.route("/signin", methods=['GET', 'POST'])
def signin():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Signin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email or password', 'danger')
    return render_template('signin.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
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
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    first_letter = current_user.username[0].upper()  # Get the first letter of the username
    if current_user.image_file != 'default.jpg':
        image_file = url_for('static', filename='image/' + current_user.image_file)
    else:
        image_file = None
    return render_template('account.html', image_file=image_file, form=form, first_letter=first_letter)

@users.route("/user/<string:username>")
def artist_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Artwork.query.filter_by(uploader=user).order_by(Artwork.date_posted.desc()).all()
    total_posts = len(posts)
    return render_template('artist_posts.html', posts=posts, user=user, total_posts=total_posts)

@users.route("/artists")
def artists():
    users = User.query.filter_by(is_artist='artist').all()
    user_posts = {}

    for user in users:
        # Count total artworks (posts) for each artist
        total_posts = Artwork.query.filter_by(uploader=user).count()
        user_posts[user.id] = total_posts
    return render_template('artists.html', users=users, user_posts=user_posts)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        except Exception as e:
            app.logger.error(f"Error sending email: {e}")
            flash('Failed to send the reset email. Please try again later.', 'danger')
        return redirect(url_for('users.signin'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.signin'))
    return render_template('reset_token.html', title='Reset Password', form=form)

