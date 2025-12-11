from flask import Flask
import pika
import json

app = Flask(__name__)

message = {'id': 1, 'name': 'name1'}

@app.route('/')
def hello_world():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=''))
    channel = connection.channel()
    channel.queue_declare(queue='Test', durable=False)
    channel.basic_publish(
        exchange='',
        routing_key='Test',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()
    return 'sent'


if __name__ == '__main__':
    app.run(host='0.0.0.0')


