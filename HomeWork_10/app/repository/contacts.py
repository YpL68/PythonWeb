from datetime import datetime
from mongoengine import *

from app.db_models import Contact
from app.function import sanitize_phone_num, email_validate


def get_contacts(filter_str: str = None) -> list:
    out_list = []
    try:
        if filter_str:
            contacts = Contact.objects(
                Q(first_name__icontains=f"{filter_str}") |
                Q(last_name__icontains=f"{filter_str}") |
                Q(phones__icontains=f"{filter_str}")).order_by("first_name")
        else:
            contacts = Contact.objects().order_by("first_name")
        if contacts:
            out_list.extend([contact.data_view for contact in contacts])
    except Exception as err:
        raise ValueError(str(err))

    return out_list


def contact_insert_or_update(data_view: dict) -> tuple:
    result = ("Operation was successful", "success")
    try:
        if data_view["id"] != "0":
            contact = Contact.objects.get(id=data_view["id"])
            if not contact:
                raise ValueError(f"No contact was found.")
        else:
            contact = Contact()

        contact.first_name = data_view["first_name"]
        contact.last_name = data_view["last_name"] if data_view["last_name"] else None
        email = data_view["email"] if data_view["email"] else None
        email_validate(email)
        contact.email = email
        contact.birthday = datetime.strptime(data_view["birthday"], "%Y-%m-%d") if data_view["birthday"] else None
        contact.address = data_view["address"] if data_view["address"] else None
        contact.phones = [sanitize_phone_num(phone) for phone in
                          list(filter(lambda x: x != "", data_view["phone_list"].lower().split(",")))]

        contact.save()
    except Exception as err:
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result


def contact_delete(cnt_id: str):
    result = ("Operation was successful", "success")
    try:
        contact = Contact.objects.get(id=cnt_id)
        if not contact:
            raise ValueError(f"Contact by id {cnt_id} not found.")

        contact.delete()
    except Exception as err:
        result = (f"Operation was aborted: {str(err)}", "danger")

    return result
