from faker import Faker
from random import choice


from connect_mongo import connect_to_db
from models import Contact, RemaindBy
from  connect_rebbit import get_channel, create_queues

connect_to_db("reminder")

fake = Faker()

CONTACT_COUNT = 20

def get_fake_contact():
    data = {
        "fullname": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "remaind_by": choice(list(RemaindBy))
    }

    return data


def fill_contacts() -> list[Contact]:
    contacts = []
    for _ in range(CONTACT_COUNT):
        fake_contact = get_fake_contact()
        contact = Contact(**fake_contact)
        contact.save()
        contacts.append(contact)
    return contacts


def main():
    with get_channel() as channel:
        exchange_name = 'reminder'
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
        channel = create_queues(channel, exchange=exchange_name)

        contacts = fill_contacts()
        for contact in contacts:
            channel.basic_publish(exchange=exchange_name, routing_key=contact.remaind_by.name, body=str(contact.pk).encode())
            print(f" [x] Sent {contact.remaind_by.name} to {contact.fullname}")
    

if __name__ == '__main__':
    main()