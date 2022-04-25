import sys
import time
import sqlite3
from PIL import Image
from urllib import response
import pika
import uuid


class ImageRpcClient(object):

  def __init__(self, host='localhost'):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat=0))

    self.channel = self.connection.channel()

    result = self.channel.queue_declare(queue='', exclusive=True)
    self.callback_queue = result.method.queue

    self.channel.basic_consume(
        queue=self.callback_queue,
        on_message_callback=self.on_response,
        auto_ack=True)

  def on_response(self, ch, method, props, body):
    if self.corr_id == props.correlation_id:
      self.response = body

  def call(self, message):
    self.response = None
    self.corr_id = str(uuid.uuid4())
    self.channel.basic_publish(
        exchange='',
        routing_key='rpc_tensor_queue',
        properties=pika.BasicProperties(
            reply_to=self.callback_queue,
            correlation_id=self.corr_id,
        ),
        body=str(message))
    while self.response is None:
      self.connection.process_data_events()
    return self.response

tensorflow_rpc = None

class AppDB:
  sqlite_insert_blob_query = """ INSERT INTO Image
                            (name, img, height, width) VALUES (?, ?, ?, ?)"""
  def __init__(self) -> None:
    self.con = sqlite3.connect('example.db')
    self.cur = self.con.cursor()
    self.cur.execute("DROP TABLE IF EXISTS Image")
    self.cur.execute('''CREATE TABLE Image (name, img, height, width)''')
    self.con.commit()

app_db = AppDB()


def bytes_len(n):
  # image = Image.open()
  # return image.height, image.width
  
  # print(type(n))
  # print(len(n))
  # print(n[0], '-', len(n[1]), n[2], n[3])
  # image = Image.frombytes('RGB', (n[2], n[3]), n[1])

  # print(image)
  # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
  response = tensorflow_rpc.call(n)
  print('tensorflow response', response)
  app_db.cur.execute(app_db.sqlite_insert_blob_query, n)
  app_db.con.commit()
  # for row in cur.execute('SELECT * FROM Image ORDER BY name'):
      # print(row)

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
  if len(sys.argv) > 2:
    if sys.argv[2] == 'sleep':
      time.sleep(10)
  host = sys.argv[1]

  tensorflow_rpc = ImageRpcClient(host=host)

  connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat=0))

  channel = connection.channel()

  channel.queue_declare(queue='rpc_queue')


  channel.basic_qos(prefetch_count=1)
  # channel.queue_delete(queue='rpc_queue')
  channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

  print(" [x] Awaiting RPC requests")
  channel.start_consuming()
finally:
  app_db.con.close()
