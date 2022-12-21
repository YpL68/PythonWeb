from datetime import datetime

from sqlalchemy import or_

from app import db
from app.db_models import Contact, Phone
from app.function import sanitize_phone_num, email_validate
# from app.constants import DATE_FORMAT


def get_contacts(filter_str: str = None) -> list:
    out_list = []
    try:
        if filter_str:
            f_str = f"%{filter_str}%"
            contacts = db.session.query(Contact).distinct() \
                .outerjoin(Phone) \
                .filter(or_(Contact.first_name.like(f_str),
                            Contact.last_name.like(f_str),
                            Phone.phone_num.like(f_str))) \
                .order_by(Contact.first_name) \
                .all()
        else:
            contacts = db.session.query(Contact).all()
        if contacts:
            out_list.extend([contact.data_view for contact in contacts])
    except Exception as err:
        db.session.rollback()
        raise ValueError(str(err))

    return out_list


def contact_phone_list_syn(contact: Contact, phone_list: list):
    phone_for_delete = []
    phone_for_append = []

    for phone in contact.phone_list:
        if phone.phone_num in phone_list:
            phone_list.remove(phone.phone_num)
        else:
            phone_for_delete.append(phone)

    for phone_num in phone_list:
        phone = db.session.query(Phone).filter(Phone.phone_num == phone_num).first()
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


def contact_insert_or_update(data_view: dict) -> tuple:
    result = ("Operation was successful", "success")
    try:
        if data_view["id"] != -1:
            contact = db.session.query(Contact).get(data_view["id"])
            if not contact:
                raise ValueError(f"Contact by id {data_view['id']} not found.")
        else:
            contact = Contact()

        contact.first_name = data_view["first_name"]
        contact.last_name = data_view["last_name"] if data_view["last_name"] else None
        email = data_view["email"] if data_view["email"] else None
        email_validate(email)
        contact.email = email
        contact.birthday = datetime.strptime(data_view["birthday"], "%Y-%m-%d") if data_view["birthday"] else None
        contact.address = data_view["address"] if data_view["address"] else None
        phone_list = [sanitize_phone_num(phone) for phone in
                      list(filter(lambda x: x != "", data_view["phone_list"].lower().split(",")))]
        contact_phone_list_syn(contact, phone_list)

        db.session.add(contact)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result


def contact_delete(cnt_id: int):
    result = ("Operation was successful", "success")
    try:
        contact = db.session.query(Contact).get(cnt_id)
        if not contact:
            raise ValueError(f"Contact by id {cnt_id} not found.")
        db.session.delete(contact)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result
