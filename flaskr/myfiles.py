from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for, send_from_directory
)
import os
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('myfiles', __name__,url_prefix='/files')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'doc', 'pptx', 'ppt', 'pptm', 'xlts'])

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT id, author_id, title, created'
        ' FROM post'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('myfiles/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        error = None
        if not title or '.' in title:
            error = 'Title is empty or invalid.'
        if file.filename == '':
            error = 'No selected file'
        extension = file.filename.rsplit('.', 1)[1].lower()
        db = get_db()
        if db.execute(
            'SELECT title FROM post WHERE title = ?',(title,)
        ).fetchone() is not None:
            error = 'Title {} is already used.'.format(title)
        if error == None and file and extension in ALLOWED_EXTENSIONS:
            db.execute(
                'INSERT INTO post (title, extension, author_id)'
                ' VALUES (?, ?, ?)',
                (title, extension, g.user['id'])
            )
            db.commit()
            filename = title + '.' + extension
            file.save(os.path.join(current_app.config['INSTANCE_PATH']+'/',filename))
            return redirect(url_for('myfiles.index'))
        else:
            error = "file extention not permited by the server"
        if error is not None:
            flash(error)
    return render_template('myfiles/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT id, extension, title, created, author_id'
        ' FROM post'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/download/<int:id>', methods=('GET', 'POST'))
def download(id):
    post = get_post(id,False)
    filename = post['title'] + '.' + post['extension']
    return send_from_directory(current_app.config['INSTANCE_PATH'], filename)

@bp.route('/delete/<int:id>', methods=('POST','GET'))
@login_required
def delete(id):
    post = get_post(id)
    db = get_db()
    path = current_app.config['INSTANCE_PATH'] + "/" + post['title'] + '.' + post['extension']
    os.remove(path);
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('myfiles.index'))
