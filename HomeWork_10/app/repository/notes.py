from mongoengine import *

from app import cache

from app.db_models import Note


def get_notes(filter_str: str = None) -> list:
    out_list = []
    try:
        if filter_str:
            notes = Note.objects(
                Q(header__icontains=f"{filter_str}") |
                Q(tags__icontains=f"{filter_str}")).order_by("header")
        else:
            notes = Note.objects().order_by("header")
        if notes:
            out_list.extend([note.data_view for note in notes])
    except Exception as err:
        raise ValueError(str(err))

    return out_list


@cache
def get_note(note_id) -> Note:
    return Note.objects.get(id=note_id)


def note_insert_or_update(data_view: dict):
    result = ("Operation was successful", "success")
    try:
        if data_view["id"] != "0":
            note = get_note(data_view["id"])
            if not note:
                raise ValueError("No note was found")
        else:
            note = Note()

        note.header = data_view["header"]
        note.content = data_view["content"]
        note.tags = [tag.strip() for tag in list(filter(lambda x: x != "", data_view["tag_list"].lower().split(",")))]

        note.save()
    except Exception as err:
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result


def note_delete(note_id: str):
    result = ("Operation was successful", "success")
    try:
        note = get_note(note_id)
        if not note:
            raise ValueError(f"Note by id {note_id} not found.")
        note.delete()
    except Exception as err:
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result
