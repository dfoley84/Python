import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(''))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print("Message Sent")
connection.close()

