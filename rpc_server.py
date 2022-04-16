import time
import sqlite3
from PIL import Image
from urllib import response
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


con = sqlite3.connect('example.db')
cur = con.cursor()
cur.execute('''CREATE TABLE Image
               (name, img, height, width)''')
sqlite_insert_blob_query = """ INSERT INTO Image
                          (name, img, height, width) VALUES (?, ?, ?, ?)"""
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def bytes_len(n):
  # image = Image.open()
  # return image.height, image.width
  
  print(type(n))
  print(len(n))
  print(n[0], '-', len(n[1]), n[2], n[3])
  # image = Image.frombytes('RGB', (n[2], n[3]), n[1])

  # print(image)
  # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
  cur.execute(sqlite_insert_blob_query, n)
  con.commit()
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
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("--- %s seconds ---" % (time.time() - start_time))

channel.basic_qos(prefetch_count=1)
# channel.queue_delete(queue='rpc_queue')
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()

con.close()
