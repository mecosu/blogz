from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

blog_posts = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_post = request.form['blog-post']
        blog_posts.append(blog_post)

    return render_template('blog.html',title="Blog", blog_posts=blog_posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    return render_template('newpost.html')

app.run()
