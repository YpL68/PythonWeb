from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db_models import Contact, Phone


def get_contact_data_view(session: Session, cnt_id) -> dict:
    if cnt_id == -1:
        return {"id": -1, "first_name": "", "last_name": "", "email": "", "birthday": "",
                "address": "", "phone_list": []}
    else:
        contact = session.query(Contact).get(cnt_id)
        if not contact:
            raise ValueError(f"Contact by id {cnt_id} not found.")
        return contact.data_view


def get_contacts(session: Session, filter_str: str = None) -> list:
    out_list = []
    if filter_str:
        f_str = f"%{filter_str}%"
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
        out_list.extend([contact.data_view for contact in contacts])

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
                raise ValueError(f"Attempting to add a phone number {phone_num}, "
                                 f"belonging to a contact {phone.contact_id}.")
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
