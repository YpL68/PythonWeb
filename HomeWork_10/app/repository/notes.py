from app import db
from app.db_models import Note


def get_notes(filter_str: str = None) -> list:
    out_list = []
    try:
        f_str = f"%{filter_str}%"
        if filter_str:
            notes = db.session.query(Note).distinct() \
                .outerjoin(NotesTags).outerjoin(Tag) \
                .filter(or_(Note.header.like(f_str), Tag.name.like(f_str))) \
                .order_by(Note.header) \
                .all()
        else:
            notes = db.session.query(Note).all()

        if notes:
            out_list.extend([note.data_view for note in notes])
    except Exception as err:
        db.session.rollback()
        raise ValueError(str(err))

    return out_list


def note_tag_list_syn(note: Note, tag_list: list):
    tag_for_delete = []
    tag_for_append = []

    for tag in note.tags:
        if tag.name in tag_list:
            tag_list.remove(tag.name)
        else:
            tag_for_delete.append(tag)

    for tag_name in tag_list:
        tag = db.session.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        tag_for_append.append(tag)

    [note.tags.remove(tag) for tag in tag_for_delete]
    note.tags.extend(tag_for_append)


def note_insert_or_update(data_view: dict):
    result = ("Operation was successful", "success")
    try:
        if data_view["id"] != -1:
            note = db.session.query(Note).get(data_view["id"])
            if not note:
                raise ValueError("No note was found")
        else:
            note = Note()

        note.header = data_view["header"]
        note.content = data_view["content"]
        tag_list = [tag.strip() for tag in list(filter(lambda x: x != "", data_view["tag_list"].lower().split(",")))]
        note_tag_list_syn(note, tag_list)
        db.session.add(note)

        db.session.commit()
    except Exception as err:
        db.session.rollback()
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result


def note_delete(note_id: int):
    result = ("Operation was successful", "success")
    try:
        note = db.session.query(Note).get(note_id)
        if not note:
            raise ValueError(f"Note by id {note_id} not found.")
        db.session.delete(note)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result
