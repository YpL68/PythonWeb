from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.constants import DATE_FORMAT
from app.function import format_phone_num


notes_tags = db.Table(
    "notes_tags",
    db.metadata,
    db.Column("note_id", None, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", None, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class NotesTags:
    note_id = None
    tag_id = None


mapper(NotesTags, notes_tags)


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    created_on = db.Column(DateTime, nullable=False, server_default=now())
    updated_on = db.Column(DateTime, nullable=False, server_default=now(), onupdate=now())


class Contact(BaseModel):
    __tablename__ = "contacts"

    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64))

    @hybrid_property
    def full_name(self):
        return self.first_name + (f" {self.last_name}" if self.last_name else "")

    email = db.Column(db.String(64), unique=True)
    birthday = db.Column(DateTime)
    address = db.Column(db.String(128))
    phone_list = relationship("Phone", cascade="all, delete-orphan", back_populates="contact")

    @hybrid_property
    def data_view(self) -> dict:
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name if self.last_name else "",
                "full_name": self.full_name,
                "email": self.email if self.email else "",
                "birthday": self.birthday.strftime(DATE_FORMAT) if self.birthday else "",
                "address": self.address if self.address else "",
                "phone_list": ", ".join([format_phone_num(phone.phone_num) for phone in self.phone_list])}


class Phone(BaseModel):
    __tablename__ = "phones"

    contact_id = db.Column(None, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False, index=True, unique=True)
    contact = relationship("Contact", back_populates="phone_list")


class Note(BaseModel):
    __tablename__ = "notes"

    header = db.Column(db.String(64), nullable=False, index=True, unique=True)
    content = db.Column(db.String(512))
    tags = relationship("Tag", secondary=notes_tags, back_populates="notes")

    @hybrid_property
    def data_view(self) -> dict:
        return {"id": self.id,
                "header": self.header,
                "content": self.content,
                "tag_list": ", ".join([tag.name for tag in self.tags])}


class Tag(BaseModel):
    __tablename__ = 'tags'

    name = db.Column(db.String(16), nullable=False, index=True, unique=True)
    notes = relationship("Note", secondary=notes_tags, back_populates="tags")
