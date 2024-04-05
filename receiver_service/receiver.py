import asyncio
import json
from datetime import datetime

import pika


async def receive_request():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='request_queue')
    channel.queue_declare(queue='processor_queue')

    def callback(ch, method, properties, body):
        request = json.loads(body)
        receive_time = datetime.now()
        request['receive_time'] = receive_time
        data = json.dumps(request)
        ch.basic_publish(exchange='', routing_key='processor_queue', body=data)

    channel.basic_consume(queue='request_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for requests...')
    channel.start_consuming()


if __name__ == '__main__':
    asyncio.run(receive_request())
