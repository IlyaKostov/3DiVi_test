import json
import pika


async def write_to_txt(data):
    request = data.get('request')
    request_id = request.get('id')
    receive_time = data.get('receive_time')
    write_time = data.get('write_time')
    if write_time:
        with open('processed_requests', 'a') as file:
            file.write(f"{request_id} | {receive_time} | {write_time}\n")
    else:
        with open('received_requests', 'a') as file:
            file.write(f"{request_id} | {receive_time}\n")


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='processor_queue')


    def callback(ch, method, properties, body):
        data = json.loads(body)
        write_to_txt(data)


    channel.basic_consume(queue='processor_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for requests...')
    channel.start_consuming()
