from PIL import Image
import time
import pika
import uuid

class ImageRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

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

c = 0
image_rpc = ImageRpcClient()
while True:
  start_time = time.time()
  image_path = '0_11.jpg'
  # img = Image.open(image_path)
  # img_height = img.height
  # img_width = img.width
  # img = img.tobytes()
  file = open(image_path, 'rb')
  blobData = file.read()
  print(" [x] Requesting image(x)")
  # response = image_rpc.call("abcdefghijklmnopqrstuvwxyz")
  # response = image_rpc.call([image_path, img, img_height, img_width])
  response = image_rpc.call([image_path, blobData, 0, 0])
  print(" [.] Got %r" % response)
  c+=1
  print('count', c)
  print("--- %s seconds ---" % (time.time() - start_time))
  # break