from sqlite3 import IntegrityError

from flask import render_template, request, redirect, url_for, flash
from app import db
from app.repository.notes import get_notes, note_delete, note_insert_or_update

from . import app


@app.route('/healthcheck', strict_slashes=False)
def healthcheck():
    return 'I am working cool'


@app.route('/', strict_slashes=False)
@app.route('/index', strict_slashes=False)
def index():
    return render_template("pages/index.html", title='Free Assistant!', auth='Yuri')


@app.route('/notes', strict_slashes=False)
def notes():
    notes_ = get_notes(db.session, filter_str="")
    return render_template('pages/notes.html', title='Notes', notes=notes_)
    # return render_template('pages/test_click.html')


@app.route('/notes/delete/<int:note_id>', methods=['POST'], strict_slashes=False)
def delete_note(note_id):
    try:
        result = note_delete(db.session, note_id), "success"
    except (ValueError, KeyError, IndexError, IntegrityError) as err:
        result = err, "danger"
    if result:
        flash(*result)
    return redirect(url_for("notes"))


@app.route('/notes/edit/<int:note_id>', methods=['POST'], strict_slashes=False)
def edit_note(note_id):
    tags_str = request.form.get("tags")
    tag_list = list(filter(lambda x: x != "", tags_str.lower().split(",")))

    data_view = {
        "id": note_id if note_id else -1,
        "header": request.form.get("header"),
        "content": request.form.get("content"),
        "tag_list": [tag.strip() for tag in tag_list]}

    try:
        result = note_insert_or_update(db.session, data_view), "success"
    except (ValueError, KeyError, IndexError, IntegrityError) as err:
        result = err, "danger"
    if result:
        flash(*result)
    return redirect(url_for("notes"))
