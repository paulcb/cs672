import sys
import time
from PIL import Image
from urllib import response
import pika

def bytes_len(n):
  pass
  # return image

def on_request(ch, method, props, body):
    start_time = time.time()
    n = body.decode("utf-8")
    import ast
    filedata = ast.literal_eval(n)
    # print(" [.] fib(%s)" % n)
    # response = fib(n)
    response = bytes_len(filedata)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("--- %s seconds ---" % (time.time() - start_time))
try:
  host = sys.argv[1]
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=host))

  channel = connection.channel()

  channel.queue_declare(queue='rpc_queue')


  channel.basic_qos(prefetch_count=1)
  # channel.queue_delete(queue='rpc_queue')
  channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

  print(" [x] Awaiting RPC requests")
  channel.start_consuming()
finally:
  pass
