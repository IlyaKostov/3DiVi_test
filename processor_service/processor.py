import asyncio
import json
import time
from datetime import datetime

import pika


async def process_request(data):
    request = data.get('request')
    delay = request.get('delay')
    await asyncio.sleep(delay)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='processor_queue')

    def callback(ch, method, properties, body):
        request = json.loads(body)
        print("Processing request:", request)
        process_request(request)
        write_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request['write_time'] = write_time
        data = json.dumps(request)
        ch.basic_publish(exchange='', routing_key='processor_queue', body=data)

    channel.basic_consume(queue='processor_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for requests...')
    channel.start_consuming()
