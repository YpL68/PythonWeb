from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.db_models import Note, NotesTags, Tag
from database.db import session_scope


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

    print(notes)

    if notes:
        out_list.append([key for key in notes[0].data_view])
        for note in notes:
            out_list.append([value for value in note.data_view.values()])

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
            raise ValueError("Заметка не найдена")
    else:
        note = Note()

    note.header = data_view["header"]
    note.content = data_view["content"]

    note_tag_list_syn(session, note, data_view["tag_list"])
    session.add(note)

    session.commit()


def note_delete(session: Session, note_id: int):
    note = session_.query(Note).get(note_id)
    if note:
        session.delete(note)
        session.commit()


if __name__ == '__main__':
    with session_scope() as session_:
        try:
            # data_note = {"id": -1,
            #              "header": "Первый пошел 10",
            #              "content": "Хрен вам, а не контент 6",
            #              "tag_list": ["Вася", "Ася", "Коля", "Моня", "jjkdjkdf"]}
            # note_create(session_, data_note)
            note_delete(session_, 30)

            # note1 = session_.query(Note).get(31)
            # data_note1 = note1.data_view
            # data_note1["tag_list"] = ["Вася", "Игорь"]
            # note_update(session_, data_note1)
        except Exception as err:
            print(err)
            if session_.in_transaction():
                session_.rollback()
