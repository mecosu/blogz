from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import cgi
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True    
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.datetime = datetime.now()
        self.date = datetime.now().date()
        self.owner = owner

    def __repr__(self):
        return '<Blog %r)>' % (self.title, self.body)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/newpost", methods=['POST'])
def add_new_post():
    body = request.form.get('body')
    title = request.form.get('title')

    if body == "":
        blog_body_blank_error = "Please fill in the body."
    else: blog_body_blank_error = ""

    if title == "":
        blog_title_blank_error = "Please fill in the title."
    else: blog_title_blank_error = ""

    if not blog_title_blank_error and not blog_body_blank_error:
            if request.method == 'POST':
                new_blog = Blog(title, body)
                db.session.add(new_blog)
                db.session.commit()
                url = "/blog?id=" + str(new_blog.id)
                return redirect(url)
    else:
        return render_template('newpost.html', blog_body_blank_error = blog_body_blank_error, blog_title_blank_error = blog_title_blank_error)

@app.route("/blog", methods=['GET', 'POST'])
def display_blog_posts():
    blog_id = request.args.get('id')
    if (blog_id):
        blog_post = Blog.query.get(blog_id)
        return render_template('single-post.html', blog_post = blog_post)

    blogs = Blog.query.order_by(desc(Blog.datetime))
    return render_template('blog.html', blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.order_by(desc(Blog.datetime))
    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    return render_template('newpost.html')

if __name__ == "__main__":
    app.run()
