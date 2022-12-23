from flask import render_template, request, redirect, url_for, flash
from app.repository.contacts import get_contacts, contact_delete, contact_insert_or_update

from . import app


@app.route('/healthcheck', strict_slashes=False)
def healthcheck():
    return 'I am working cool'


@app.route('/', strict_slashes=False)
@app.route('/index', strict_slashes=False)
def index():
    return render_template("pages/index.html", title='Free Assistant!', auth='Yuri')


# @app.route('/notes', methods=['GET', 'POST'], strict_slashes=False)
# def notes():
#     notes_ = []
#
#     if request.method == 'POST':
#         filter_str = request.form.get("filter_str")
#     else:
#         filter_str = ""
#
#     try:
#         notes_ = get_notes(filter_str=filter_str)
#     except ValueError as err:
#         flash(str(err), "danger")
#
#     return render_template('pages/notes.html', title='Notes',
#                            notes=notes_, filter_str=filter_str)
#
#
# @app.route('/notes/delete/<int:note_id>', methods=['POST'], strict_slashes=False)
# def delete_note(note_id):
#     result = note_delete(note_id)
#     if result:
#         flash(*result)
#     return redirect(url_for("notes"))
#
#
# @app.route('/notes/edit/<int:note_id>', methods=['POST'], strict_slashes=False)
# def edit_note(note_id):
#     data_view = {
#         "id": note_id if note_id else -1,
#         "header": request.form.get("header"),
#         "content": request.form.get("content"),
#         "tag_list": request.form.get("tags")}
#
#     result = note_insert_or_update(data_view)
#     if result:
#         flash(*result)
#
#     return redirect(url_for("notes"))
#
#
@app.route('/contacts', methods=['GET', 'POST'], strict_slashes=False)
def contacts():
    contacts_ = []
    if request.method == 'POST':
        filter_str = request.form.get("filter_str")
    else:
        filter_str = ""

    try:
        contacts_ = get_contacts(filter_str=filter_str)
    except ValueError as err:
        flash(str(err), "danger")
    return render_template('pages/contacts.html', title='Contacts',
                           contacts=contacts_, filter_str=filter_str)


@app.route('/contacts/delete/<cnt_id>', methods=['POST'], strict_slashes=False)
def delete_contact(cnt_id):
    result = contact_delete(cnt_id)
    if result:
        flash(*result)
    return redirect(url_for("contacts"))


@app.route('/contacts/edit/<cnt_id>', methods=['POST'], strict_slashes=False)
def edit_contact(cnt_id):
    data_view = {
        "id": cnt_id,
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "birthday": request.form.get("birthday"),
        "email": request.form.get("email"),
        "address": request.form.get("address"),
        "phone_list": request.form.get("phones")}

    result = contact_insert_or_update(data_view)
    if result:
        flash(*result)
    return redirect(url_for("contacts"))
