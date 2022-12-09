from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.db_models import Contact, Phone, DATE_FORMAT
from function import format_phone_num

from database.db import session_scope


def get_contact_data_view(session: Session, cnt_id) -> dict:
    if cnt_id == -1:
        return {"id": -1, "first_name": "", "last_name": "", "email": "", "birthday": "",
                "address": "", "phone_list": []}
    else:
        contact = session.query(Contact).get(cnt_id)
        if not contact:
            raise ValueError(f"Contact by id {cnt_id} not found.")
        return contact.data_view


def contact_data_view_to_list(data_view: dict) -> list:
    return [
        str(data_view["id"]),
        data_view["first_name"],
        data_view["last_name"] if data_view["last_name"] else "",
        data_view["email"] if data_view["email"] else "",
        data_view["birthday"].strftime(DATE_FORMAT) if data_view["birthday"] else "",
        data_view["address"] if data_view["address"] else "",
        ", ".join([format_phone_num(phone) for phone in data_view["phone_list"]])
    ]


def get_contacts(session: Session, filter_str: str = None) -> list:
    out_list = []
    f_str = f"%{filter_str}%"
    if filter_str:
        contacts = session.query(Contact).distinct() \
            .outerjoin(Phone) \
            .filter(or_(Contact.first_name.like(f_str),
                        Contact.last_name.like(f_str),
                        Phone.phone_num.like(f_str))) \
            .order_by(Contact.first_name) \
            .all()
    else:
        contacts = session.query(Contact).all()

    if contacts:
        out_list.append([key for key in contacts[0].data_view])
        out_list.extend([contact_data_view_to_list(contact.data_view) for contact in contacts])

    session.commit()

    return out_list


def contact_phone_list_syn(session: Session, contact: Contact, phone_list: list):
    phone_for_delete = []
    phone_for_append = []

    for phone in contact.phone_list:
        if phone.phone_num in phone_list:
            phone_list.remove(phone.phone_num)
        else:
            phone_for_delete.append(phone)

    for phone_num in phone_list:
        phone = session.query(Phone).filter(Phone.phone_num == phone_num).first()
        if phone:
            print(f"Phone {phone.phone_num}")
            print(f"contact id {contact.id}")
            if not contact.id or phone.contact_id != contact.id:
                raise ValueError(f"Попытка добавить номер {phone_num}, принадлежащий контакту {phone.contact_id}.")
            else:
                phone_list.remove(phone.phone_num)
                continue
        else:
            phone_for_append.append(Phone(contact=contact, phone_num=phone_num))

    [contact.phone_list.remove(phone) for phone in phone_for_delete]
    contact.phone_list.extend(phone_for_append)


def contact_insert_or_update(session: Session, data_view: dict) -> str:
    if data_view["id"] != -1:
        contact = session.query(Contact).get(data_view["id"])
        if not contact:
            raise ValueError(f"Contact by id {data_view['id']} not found.")
    else:
        contact = Contact()

    contact.first_name = data_view["first_name"]
    contact.last_name = data_view["last_name"]
    contact.email = data_view["email"]
    contact.birthday = data_view["birthday"]
    contact.address = data_view["address"]

    contact_phone_list_syn(session, contact, data_view["phone_list"])
    session.add(contact)

    session.commit()

    return "Operation was successful"


def contact_delete(session: Session, cnt_id: int):
    contact = session.query(Contact).get(cnt_id)
    if not contact:
        raise ValueError(f"Contact by id {cnt_id} not found.")
    session.delete(contact)
    session.commit()
    return "Operation was successful"


if __name__ == '__main__':
    with session_scope() as session:
        try:
            try:
                data_view = get_contact_data_view(session, 43)
                print(data_view)
                data_view["id"] = -1
                data_view["first_name"] = data_view["first_name"] + "1"
                data_view["phone_list"] = ['380147711472', '389984587737']

                print(data_view)
                print(contact_insert_or_update(session, data_view))
            except (ValueError, KeyError, IndexError) as err:
                print(err)
        except Exception as err:
            print(err)
            if session.in_transaction():
                session.rollback()
