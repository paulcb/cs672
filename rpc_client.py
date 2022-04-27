import sys
from PIL import Image
import time
import pika
import uuid
import signal
import glob
import random 


class ImageRpcClient(object):

    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))

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

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

# outfile = open(sys.argv[2], 'w')
random.seed(12345)
files = glob.glob('Food-5K/*/*')
files_range = len(files) - 1
def signal_handler(sig, frame):
    # outfile.close()
    sys.exit(0)
signal.signal(signal.SIGTERM, signal_handler)
host = sys.argv[1]
c = 0
image_rpc = ImageRpcClient(host=host)
files_load = []
for image_path in files:
  file = open(image_path, 'rb')
  blobData = file.read()
  files_load.append((blobData, image_path))
while True:
  start_time = time.time()
  image_path = '0_11.jpg'
  # img = Image.open(image_path)
  # img_height = img.height
  # img_width = img.width
  # img = img.tobytes()
  irand = random.randrange(files_range)
  blobData, image_path = files_load[irand]
  # file = open(files[irand], 'rb')
  # blobData = file.read()
  # print(" [x] Requesting image(x)")
  # response = image_rpc.call("abcdefghijklmnopqrstuvwxyz")
  # response = image_rpc.call([image_path, img, img_height, img_width])
  response = image_rpc.call([image_path, blobData, 0, 0])
  # print(" [.] Got %r" % response)
  c+=1
  print('count', c)
  print("--- %s seconds ---" % (time.time() - start_time))
  # outfile.write("--- %s seconds ---" % str((time.time() - start_time)) + '\n')
  # outfile.write('count' + str(c) +  '\n')
  # break

