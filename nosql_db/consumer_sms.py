from time import sleep
import sys

from models import Contact, RemaindBy
from connect_mongo import connect_to_db
from connect_rebbit import get_channel

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

QUEUE_NAME = RemaindBy.sms.name

connect_to_db("reminder")

def send_sms(phone: str, message: str) -> bool:
    sleep(1)
    return True

def main():
    def proccess_message(ch, method, properties, body):
        contact_id = body.decode()
        message = f"{BLUE} Message reminder"
        contact = Contact.objects.with_id(contact_id)
        if contact is None:
            print(f"{RED} [X] invalid contact {contact_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        if send_sms(contact.phone, message):
            contact.sent = True
            contact.save()
            print(f"{GREEN} [X] Successfully sent to {contact.phone}")
        else:
            print(f"{RED} [X] Can't send message to {contact_id}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)


    with get_channel() as channel:
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=proccess_message)

        channel.start_consuming()
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'{BLUE}Interrupted{RESET}')
        sys.exit(0)

        