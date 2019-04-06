import datetime
import os

import psycopg2
from flask import Flask,render_template,url_for,redirect,request,session,flash
from werkzeug.security import check_password_hash, generate_password_hash

from database import connector

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


conf = {
    'name': os.environ['pystack_name'],
    'desc': 'Project: Pystack'
}
@app.context_processor
def inject_conf_in_all_templates():
    return dict(conf=conf)

@app.route('/')
@app.route('/index')
@app.route('/index/<status>')
def index(status=None):
    con = connector()
    cur = con.cursor()
    results = []
    cur.execute("select subject,content from bulletins where due_date >= current_date order by bulletin_id desc ")
    results.append(cur.fetchall())
    cur.close()
    cur = con.cursor()
    cur.execute("select blog_id,subject,LEFT(content,30),created_on from blogs order by blog_id desc ")
    results.append(cur.fetchall())
    cur.close()
    con.close()
    return render_template('index.html',results=results,status=status)

@app.route('/manager', methods=('get','post'))
def manager():
    status=None
    if session['group_id'] is not '0':
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['send'] == 'Create bulletin':
            subject = request.form['nb_subject']
            content = request.form['nb_content']
            con = connector()
            cur = con.cursor()
            cur.execute("INSERT INTO bulletins VALUES (DEFAULT,current_timestamp,current_timestamp,'%s','%s')" % (subject,content))
            con.commit()
            cur.close()
            con.close()
            status='bulletin posted'
            return redirect(url_for('index',status=status))
        if request.form['send'] == 'Create blog post':
            title = request.form['b_subject']
            content = request.form['b_content']
            con = connector()
            cur = con.cursor()
            cur.execute("INSERT INTO blogs VALUES (DEFAULT,current_timestamp,current_timestamp,'%s','%s')" % (title,content))
            con.commit()
            cur.close()
            con.close()
            status='blog posted'
            return redirect(url_for('index',status=status))

    return render_template('manager.html')

@app.route('/text_page')
@app.route('/text_page/<text>')
def text_page(text=None):
    return render_template('text_page.html',text=text)

@app.route('/blog/<blog_id>', methods=('get','post'))
def blog(blog_id=None):
    if request.method == 'POST':
        if request.form['send'] == 'Update blog post':
                subject = request.form['subject']
                content = request.form['content']
                con = connector()
                cur = con.cursor()
                cur.execute("UPDATE blogs SET subject='%s', content='%s' where blog_id='%s'" % (subject,content,blog_id))
                con.commit()
                cur.close()
                con.close()
                status='blog post updated'
                return redirect(url_for('index',status=status))
    if blog_id:
        con = connector()
        cur = con.cursor()
        cur.execute("select blog_id,subject,content,created_on from blogs where blog_id='%s'" % blog_id) 
        blog = cur.fetchall() 
        cur.close()
        con.close()
    return render_template('blog.html', blog=blog)

@app.route('/post_page', methods=('get','post'))
def post_page():
    status=None
    if request.method == 'POST':
        status = request.form['post_example']
    return render_template('post_page.html',status=status)

@app.route('/register', methods=('get', 'post'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = connector()
        cur = con.cursor()
        error = None
        status=None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            cur.execute("SELECT user_id FROM users WHERE username = '%s'" % username)
            if cur.fetchone() is not None:
                error = "Username '%s' can not be registered for a new account"

        if error is None:
            cur.execute("INSERT INTO users VALUES (DEFAULT,DEFAULT,current_timestamp,current_timestamp,'%s','%s')" % (username, generate_password_hash(password)))
            con.commit()
            status='user registered'
            return redirect(url_for('index',status=status))

        cur.close()
        con.close()
        flash(error % username)

    return render_template('register.html')

@app.route('/login', methods=('get','post'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error=None

        con = connector()
        cur = con.cursor()
        cur.execute("select group_id,username,password from users where username='%s' fetch first 1 rows only" % username)
        user = cur.fetchone()
        cur.close()
        con.close()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['group_id'] = user[0]
            session['user'] = user[1]
            status='logged in'
            return redirect(url_for('index',status=status))
        
        cur.close()
        con.close()
        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    status='logged out'
    return redirect(url_for('index',status=status))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')