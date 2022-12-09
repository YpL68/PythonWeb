from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.db_models import Contact, Phone, DATE_FORMAT

from function import format_phone_num


def contact_data_view_to_list(data_view: dict) -> list:
    return [
        str(data_view["id"]),
        data_view["first_name"],
        data_view["last_name"],
        data_view["email"],
        data_view["birthday"].strftime(DATE_FORMAT) if data_view["birthday"] else "",
        data_view["address"],
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
        for contact in contacts:
            out_list.append(contact_data_view_to_list(contact.data_view))

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
            if phone.contact_id != contact.id:
                raise ValueError(f"Попытка добавить номер {phone_num}, принадлежащий контакту {phone.contact_id}.")
            else:
                phone_list.remove(phone.phone_num)
                continue
        else:
            phone_for_append.append(Phone(contact=contact, phone_num=phone_num))

    [contact.phone_list.remove(phone) for phone in phone_for_delete]
    contact.phone_list.extend(phone_for_append)


def contact_insert_or_update(session: Session, data_view: dict):
    if data_view["id"] != -1:
        contact = session.query(Contact).get(data_view["id"])
        if not contact:
            raise ValueError("Контакт не найден")
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


def contact_delete(session: Session, cnt_id: int):
    contact = session.query(Contact).get(cnt_id)
    if contact:
        session.delete(contact)
        session.commit()
