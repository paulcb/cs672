import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='federate_hello')

channel.basic_publish(exchange='', routing_key='federate_hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
