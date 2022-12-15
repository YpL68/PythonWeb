from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.ext.hybrid import hybrid_property

from app import db

DATE_FORMAT = "%d.%m.%Y"

notes_tags = Table(
    "notes_tags",
    db.metadata,
    Column("note_id", None, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", None, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class NotesTags:
    note_id = None
    tag_id = None


mapper(NotesTags, notes_tags)


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, nullable=False, server_default=now())
    updated_on = Column(DateTime, nullable=False, server_default=now(), onupdate=now())


class Contact(BaseModel):
    __tablename__ = "contacts"

    first_name = Column(String(64), index=True, nullable=False)
    last_name = Column(String(64))

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name

    email = Column(String(64), unique=True)
    birthday = Column(DateTime)
    address = Column(String(128))
    phone_list = relationship("Phone", cascade="all, delete-orphan", back_populates="contact")

    @hybrid_property
    def data_view(self) -> dict:
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "birthday": self.birthday,
                "address": self.address,
                "phone_list": [phone.phone_num for phone in self.phone_list]}


class Phone(BaseModel):
    __tablename__ = "phones"

    contact_id = Column(None, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    phone_num = Column(String(12), nullable=False, index=True, unique=True)
    contact = relationship("Contact", back_populates="phone_list")


class Note(BaseModel):
    __tablename__ = "notes"

    header = Column(String(64), nullable=False, index=True, unique=True)
    content = Column(String(512))
    tags = relationship("Tag", secondary=notes_tags, back_populates="notes")

    @hybrid_property
    def data_view(self) -> dict:
        return {"id": self.id,
                "header": self.header,
                "content": self.content,
                "tag_list": ", ".join([tag.name for tag in self.tags])}


class Tag(BaseModel):
    __tablename__ = 'tags'

    name = Column(String(16), nullable=False, index=True, unique=True)
    notes = relationship("Note", secondary=notes_tags, back_populates="tags")
