import pika
from contextlib import contextmanager

from models import RemaindBy


@contextmanager
def get_channel(user_name: str="guest", password: str="guest", host: str="localhost", port: int=5672):
    try:
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
        channel = connection.channel()
    
        yield channel
    
    except Exception as error:
        print(error)
    
    finally:
        if connection:
            connection.close()

def create_queues(channel, exchange: str):
    for item in RemaindBy:
        channel.queue_declare(queue=item.name, durable=True)
        channel.queue_bind(exchange=exchange, queue=item.name)

    return channel
