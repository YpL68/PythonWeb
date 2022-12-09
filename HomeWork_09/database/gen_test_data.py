import faker

from database.db import session_scope
from database.db_models import Note, Tag, NotesTags, Contact, Phone

NUM_NOTES = 20
NUM_TAGS = 30
NUM_CONTACTS = 30

fake_data = faker.Faker('uk_UA')


def clear_data(session_):
    session_.query(NotesTags).delete(synchronize_session=False)
    session_.query(Note).delete(synchronize_session=False)
    session_.query(Tag).delete(synchronize_session=False)

    session_.query(Contact).delete(synchronize_session=False)
    session_.query(Phone).delete(synchronize_session=False)

    session_.commit()


def generate_notes(session_):
    for _ in range(NUM_NOTES):
        note = Note(
            header=fake_data.name(),
            content=fake_data.text(128)
        )
        session_.add(note)
    session_.commit()


def generate_contacts(session_):
    for _ in range(NUM_CONTACTS):
        contact = Contact(
            first_name=fake_data.first_name(),
            last_name=fake_data.last_name(),
            email=fake_data.email(),
            address=fake_data.address()
        )
        session_.add(contact)
    session_.commit()


if __name__ == '__main__':

    with session_scope() as session:
        try:
            clear_data(session)
            generate_notes(session)
            generate_contacts(session)

        except Exception as err:
            print(err)
            if session.in_transaction():
                session.rollback()
