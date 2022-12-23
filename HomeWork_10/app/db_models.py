from datetime import datetime
# from mongoengine import signals, queryset_manager, Q

from app import db
from app.constants import DATE_FORMAT
from app.function import format_phone_num


class Note(db.Document):
    created_on = db.DateTimeField(default=datetime.now())
    updated_on = db.DateTimeField(default=datetime.now())

    header = db.StringField(max_length=64, unique=True, required=True)
    content = db.StringField(max_length=512)
    tags = db.ListField(db.StringField(max_length=32))

    @property
    def data_view(self) -> dict:
        return {
                "id": str(self.id),
                "header": self.header,
                "content": self.content if self.content else "",
                "tag_list": ", ".join([tag for tag in self.tags])}


class Contact(db.Document):
    created_on = db.DateTimeField(default=datetime.now())
    updated_on = db.DateTimeField(default=datetime.now())

    id_ = db.SequenceField()
    first_name = db.StringField(max_length=64, required=True)
    last_name = db.StringField(max_length=64)
    email = db.StringField(max_length=64, unique=True)
    birthday = db.DateField()
    address = db.StringField(max_length=128)
    phones = db.ListField(db.StringField(min_lenght=12, max_length=12))

    @property
    def full_name(self):
        return self.first_name + (f" {self.last_name}" if self.last_name else "")

    @property
    def data_view(self) -> dict:
        return {"id": str(self.id),
                "first_name": self.first_name,
                "last_name": self.last_name if self.last_name else "",
                "full_name": self.full_name,
                "email": self.email if self.email else "",
                "birthday": self.birthday.strftime(DATE_FORMAT) if self.birthday else "",
                "address": self.address if self.address else "",
                "phone_list": ", ".join([format_phone_num(phone) for phone in self.phones])}
