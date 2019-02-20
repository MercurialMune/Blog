import requests
from . import main
import json
from . import main
from flask_login import login_required, current_user
from .. models import Blog, User, Comment
from flask import render_template, redirect, request, url_for, abort, flash
from .. import db
from datetime import datetime
from .forms import BlogForm, UpdateProfile, CommentForm, UpdateForm


@main.route("/")
def index():
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return render_template('index.html', random =  random)

@main.route('/blogs/')
def blog():
    blog = Blog.query.order_by(Blog.date_posted.desc())
    return render_template('/blogs.html', blog=blog)


@main.route("/blogs/details/<int:blog_id>", methods = ["GET", "POST"])
def blog_details(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        add_comment = Comment(name=name, description=description, blog_id=blog.id)
        add_comment.save_comment()
        return redirect(url_for('main.blog', blog_id=blog.id))
    comment = Comment.query.filter_by(blog_id = blog.id)
    return render_template("blog_details.html", form=form, blog=blog, comment=comment)


@main.route('/blogs/new/', methods = ["GET", "POST"])
@login_required
def add_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        owner_id = current_user
        date_posted = str(datetime.now())
        print(current_user._get_current_object().id)
        new_blog = Blog(owner_id = current_user._get_current_object().id, title = title, description=description)
        db.session.add(new_blog)
        db.session.commit()
        flash('You added a new blog', 'success')
        return redirect(url_for('main.blog'))
    return render_template('new.html', form=form)

@main.route("/remove/<blog_id>",methods = ["GET", "POST"] )
@login_required
def update_blog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    form = UpdateForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.description = form.description.data
        db.session.commit()
        flash('Blog updated!!!', 'success')
        return redirect(url_for('main.blog'))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.description.data = blog.description

    return render_template('new.html', form=form)


@main.route("/remove/<blog_id>/remove_comment",methods = ["GET", "POST"] )
@login_required
def remove_comment(blog_id):
    comment = Comment.tquery.filter_by(id = blog_id).first()
    blog_id = comment.blog_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.blog_details', blog_id = blog_id))


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    return render_template('/profiles/profile.html', user = user)



@main.route('/user/<uname>/update/avatar', methods = ['GET', 'POST'])
@login_required
def update_avatar(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return render_template('/profiles/update.html')


@main.route('/user/<uname>/update', methods = ['GET', 'POST'])
@login_required
def update(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))
    return render_template('profiles/update.html', form=form)











