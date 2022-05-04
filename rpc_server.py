import sys
import time
import sqlite3
import pika
import uuid
import ast
import psutil
import json
import os


class ImageRpcClient(object):

  def __init__(self, host='localhost'):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

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
    response = self.response.decode("utf-8")
    response = ast.literal_eval(response)
    return response

tensorflow_rpc = None
class Metrics:
  transaction = {}
  outfile = None
metrics = Metrics()
metrics.transaction['transaction_count'] = 1

m_path = 'opt/transaction_metrics.txt'
if os.path.isfile(m_path):
  os.remove(m_path)
metrics.outfile = open(m_path, 'a')

class AppDB:
  sqlite_insert_blob_query = """ INSERT INTO Image
                            (name, img, img_resize, height, width, r_height, r_width, label_string) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
  def __init__(self) -> None:
    self.con = sqlite3.connect('opt/example.db')
    self.cur = self.con.cursor()
    self.cur.execute("DROP TABLE IF EXISTS Image")
    self.cur.execute('''CREATE TABLE Image (name, img, img_resize, height, width, r_height, r_width, label_string)''')
    self.con.commit()

app_db = AppDB()


def call_func(values):
  t_out = tensorflow_rpc.call(values)
  # print(t_out[1], t_out[2], t_out[3], t_out[4], t_out[5])
  store_values = (values[0], values[1], t_out[0], t_out[1], t_out[2], t_out[3], t_out[4], t_out[5])
  app_db.cur.execute(app_db.sqlite_insert_blob_query, store_values)
  app_db.con.commit()
  # for row in cur.execute('SELECT * FROM Image ORDER BY name'):
      # print(row)

  # return 'success '
  return 'success ' + t_out[5]

def on_request(ch, method, props, body):
    start_time = time.time()
    
    n = body.decode("utf-8")
    filedata = ast.literal_eval(n)
    # print(" [.] fib(%s)" % n)
    # response = fib(n)
    response = call_func(filedata)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    t_out = 't_' + str(metrics.transaction['transaction_count'])
    metrics.transaction[t_out] = {}
    ioc_out = psutil.disk_io_counters()
    metrics.transaction[t_out]['t_num'] = metrics.transaction['transaction_count']
    metrics.transaction[t_out]['read_count'] = ioc_out.read_count
    metrics.transaction[t_out]['write_count'] = ioc_out.write_count
    metrics.transaction[t_out]['read_bytes'] = ioc_out.read_bytes
    metrics.transaction[t_out]['write_bytes'] = ioc_out.write_bytes
    metrics.transaction[t_out]['read_time'] = ioc_out.read_time
    metrics.transaction[t_out]['write_time'] = ioc_out.write_time
    try:
      metrics.transaction[t_out]['read_merged_count'] = ioc_out.read_merged_count
      metrics.transaction[t_out]['write_merged_count'] = ioc_out.write_merged_count
      metrics.transaction[t_out]['busy_time'] = ioc_out.busy_time
    except AttributeError:
      pass
    cpu_out = psutil.cpu_percent(interval=None, percpu=True)
    metrics.transaction[t_out]['cpu_perc'] = cpu_out
    cpu_times = psutil.cpu_times()
    metrics.transaction[t_out]['user'] = cpu_times.user
    metrics.transaction[t_out]['nice'] = cpu_times.nice
    metrics.transaction[t_out]['system'] = cpu_times.system
    metrics.transaction[t_out]['idle'] = cpu_times.idle
    metrics.transaction[t_out]['iowait'] = cpu_times.iowait
    metrics.transaction[t_out]['irq'] = cpu_times.irq
    metrics.transaction[t_out]['softirq'] = cpu_times.softirq
    metrics.transaction[t_out]['steal'] = cpu_times.steal
    metrics.transaction[t_out]['guest'] = cpu_times.guest
    metrics.transaction[t_out]['guest_nice'] = cpu_times.guest_nice
    netio_out = psutil.net_io_counters()
    metrics.transaction[t_out]['bytes_sent'] = netio_out.bytes_sent
    metrics.transaction[t_out]['bytes_recv'] = netio_out.bytes_recv
    metrics.transaction[t_out]['packets_sent'] = netio_out.packets_sent
    metrics.transaction[t_out]['packets_recv'] = netio_out.packets_recv
    t_time = time.time() - start_time
    metrics.transaction['t_time'] = t_time
    metric_json = json.dumps(metrics.transaction[t_out])
    metrics.outfile.write(metric_json + '\n')
    metrics.outfile.flush()
    print("--- %s seconds ---" % t_time)
    metrics.transaction['transaction_count'] = metrics.transaction['transaction_count'] + 1


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
  # outfile = open('/opt/transaction.json', 'w')
  # json.dump(metrics.transaction, outfile, indent=2)
  metrics.outfile.close()
  app_db.con.close()
