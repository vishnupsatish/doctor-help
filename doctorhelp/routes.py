import os
import secrets
import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from doctorhelp import app, db, bcrypt, mail, admin
from doctorhelp.forms import (RegistrationForm, DoctorRegistrationForm, LoginForm, PostForm, CategorySearchForm)
from doctorhelp.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_admin.contrib.sqla import ModelView

class AdminView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            abort(404)

        if current_user.admin:
            return True

        abort(404)

class UserView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            abort(404)

        if current_user.admin and (current_user.email == "vishnupavan.satish@gmail.com" or current_user.email == "pranavrao145@gmail.com" or current_user.email == "lavansurendra@gmail.com"):
            return True

        abort(404)


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))


@app.route("/")
@app.route("/home")
def home():
    if not current_user.is_authenticated:
        flash("You need to log in to view your personalized home page. For now, you can view all of the posts.", "info")
        return redirect(url_for('all_posts'))
    if current_user.doctor:
        posts = Post.query.order_by(Post.date.desc()).all()
        relevant_posts = []
        for post in posts:
            if len(relevant_posts) == 5:
                break
            if len(list(set(post.fields.split(",")) & set(current_user.fields.split(",")))):
                relevant_posts.append(post)
        return render_template('home_doctor.html', current_user=current_user, posts=relevant_posts, page_title="Home")
    posts = Post.query.filter_by(author=current_user)
    return render_template('home_patient.html', current_user=current_user, posts=posts, page_title="Home")



@app.route('/register')
def register():
    return render_template("register.html", page_title="Register")


@app.route("/register/patient", methods=['GET', 'POST'])
def register_patient():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(admin=False, username=form.username.data, email=form.email.data, password=hashed_password, doctor=False, gender=form.gender.data, dob=datetime.datetime.strptime(form.dob.data, "%b %d, %Y"), name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register_patient.html', title='Register', form=form, page_title="Register as Patient")


@app.route("/register/doctor", methods=['GET', 'POST'])
def register_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(admin=False, username=form.username.data, email=form.email.data, password=hashed_password, fields=",".join(form.fields.data), doctor=True, name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register_doctor.html', title='Register', form=form, page_title="Register as Doctor")



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.doctor == form.doctor_or_patient.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form, page_title="Login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/new', methods=["GET", "POST"])
@login_required
def new():
    if current_user.doctor:
        flash("Doctors do not have permission to ask for advice.", 'warning')
        return redirect(url_for('home'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, title=form.title.data, anonymous=form.anonymous.data, user_id=current_user.id, fields=",".join(form.fields.data))
        db.session.add(post)
        db.session.commit()
        flash("Your question has successfully been posted!", "success")
        return redirect(url_for('specific_post', id=post.id))
    return render_template('new.html', form=form, page_title="New")


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@app.route('/post/<int:id>', methods=["GET", "POST"])
def specific_post(id):
    if request.method == "POST":
        comment_content = request.values.get('comment')
        comment = Comment(content=comment_content, user_id=current_user.id, post_id=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('specific_post', id=id))
    post = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(post_id=id)
    doctor_comment_tags = dict()
    for comment in comments:
        if comment.author.doctor:
            doctor_comment_tags[comment] = list(set(post.fields.split(",")) & set(comment.author.fields.split(",")))
        else:
            doctor_comment_tags[comment] = []
    fields = post.fields.split(",")
    age = calculate_age(post.author.dob)
    name = post.author.name
    username = post.author.username
    if post.anonymous == True:
        name = "Anonymous"
        username = "Anonymous"
    return render_template('post.html', age=age, name=name, fields=fields, post=post, comments=comments, current_user=current_user, doctor_comment_tags=doctor_comment_tags, username=username, page_title="Post")

@app.route('/about')
def about():
    return render_template('about.html', page_title="About")


@app.route("/posts/all")
def all_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('view_posts.html', posts=posts, current_page="all_posts", categories="", page_title="All Posts")

@app.route('/category', methods=["GET", "POST"])
def category():
    categories = request.args.get('categories', None)
    print(categories)
    if categories == None:
        form = CategorySearchForm()
        if form.validate_on_submit():
            return redirect(url_for('category', categories=",".join(form.category.data)))
        return render_template('search_category.html', form=form, page_title="Category Search")
    posts = Post.query.order_by(Post.date.desc())
    relevant_posts = []
    for post in posts:
        if len(relevant_posts) == 5:
            break
        if len(list(set(post.fields.split(",")) & set([x for x in categories.split(',')]))) > 0:
            relevant_posts.append(post)
    print(relevant_posts)
    return render_template('category_posts.html', posts=relevant_posts, results=str(len(relevant_posts)) + " results for the categories " + categories.replace(",", ", "), page_title="Category Search")



@app.route('/profile/<username>')
def profile(username):
    doctor = User.query.filter_by(username=username, doctor=True).first_or_404()
    return render_template("doctorprofile.html", doctor=doctor, page_title=username + " Profile")