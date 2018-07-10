from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True    
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r)>' % (self.title, self.body)

@app.route("/newpost", methods=['POST'])
def add_new_post():
    body = request.form.get('body')
    title = request.form.get('title')

    if request.method == 'POST':
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    return render_template('newpost.html')

if __name__ == "__main__":
    app.run()
