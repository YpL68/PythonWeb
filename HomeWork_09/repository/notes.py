from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.db_models import Note, NotesTags, Tag


def get_note_data_view(session: Session, note_id) -> dict:
    if note_id == -1:
        return {"id": -1, "header": "", "content": "", "tags": []}
    else:
        note = session.query(Note).get(note_id)
        if not note:
            raise ValueError(f"Note by id {note_id} not found.")
        return note.data_view


def note_data_view_to_list(data_view: dict) -> list:
    return [
        str(data_view["id"]),
        data_view["header"],
        data_view["content"] if data_view["content"] else "",
        ", ".join([tag for tag in data_view["tag_list"]])
    ]


def get_notes(session: Session, filter_str: str = None) -> list:
    out_list = []
    f_str = f"%{filter_str}%"
    if filter_str:
        notes = session.query(Note).distinct() \
            .outerjoin(NotesTags).outerjoin(Tag) \
            .filter(or_(Note.header.like(f_str), Tag.name.like(f_str))) \
            .order_by(Note.header) \
            .all()
    else:
        notes = session.query(Note).all()

    if notes:
        out_list.append([key for key in notes[0].data_view])
        out_list.extend([note_data_view_to_list(note.data_view) for note in notes])

    return out_list


def note_tag_list_syn(session: Session, note: Note, tag_list: list):
    tag_for_delete = []
    tag_for_append = []

    for tag in note.tags:
        if tag.name in tag_list:
            tag_list.remove(tag.name)
        else:
            tag_for_delete.append(tag)

    for tag_name in tag_list:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        tag_for_append.append(tag)

    [note.tags.remove(tag) for tag in tag_for_delete]
    note.tags.extend(tag_for_append)


def note_insert_or_update(session: Session, data_view: dict):
    if data_view["id"] != -1:
        note = session.query(Note).get(data_view["id"])
        if not note:
            raise ValueError("No note was found")
    else:
        note = Note()

    note.header = data_view["header"]
    note.content = data_view["content"]

    note_tag_list_syn(session, note, data_view["tag_list"])
    session.add(note)

    session.commit()

    return "Operation was successful"


def note_delete(session: Session, note_id: int):
    note = session.query(Note).get(note_id)
    if not note:
        raise ValueError(f"Note by id {note_id} not found.")
    session.delete(note)
    session.commit()
    return "Operation was successful"
