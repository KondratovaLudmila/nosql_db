from mongoengine import Document
from mongoengine.fields import DateField, ListField, StringField, ReferenceField, EmailField, BooleanField, EnumField
from enum import Enum


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateField()
    born_location = StringField()
    description = StringField()
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(document_type=Author, reverse_delete_rule=1)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}

class RemaindBy(Enum):
    email = 1
    sms = 2

class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField()
    phone = StringField()
    remaind_by = EnumField(RemaindBy, default=RemaindBy.email)
    sent = BooleanField(default=False)
    meta = {'collection': 'contacts'}

    

