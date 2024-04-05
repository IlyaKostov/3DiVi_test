import logging

import pika
import json
import random
import asyncio

logging.basicConfig(level=logging.INFO, filename='client_log.log', filemode='a',
                    format='%(asctime)s - Thread %(thread)d - %(message)s')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='requests_queue')


async def send_requests(connection_count, connection_value, delay_range):
    for i in range(connection_count):
        await asyncio.gather(*[send_request(i+1, delay_range) for i in range(connection_value)])
    connection.close()


async def send_request(request_id, delay_range):
    delay = random.randint(*delay_range)
    request = {
        'request': {
            'id': request_id,
            'delay': delay
        }
    }

    logging.info(request)

    data = json.dumps(request)
    channel.basic_publish(exchange='', routing_key='requests_queue', body=data)


if __name__ == '__main__':
    asyncio.run(send_requests(connection_count=5, connection_value=20, delay_range=(1, 6)))


