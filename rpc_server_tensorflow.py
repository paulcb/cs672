import sys
import time
from PIL import Image
from urllib import response
import pika
import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16

# load the model
model = VGG16()

def bytes_len(n):
  # start_time = time.time()
  image = tf.io.decode_jpeg(n[1])
  # print("1--- %s seconds ---" % (time.time() - start_time))

  # start_time = time.time()
  # image = load_img(image, target_size=(224, 224))
  image = tf.image.resize(image, [224, 224])
  # print("2--- %s seconds ---" % (time.time() - start_time))

  # start_time = time.time()
  image = img_to_array(image)
  # print("3--- %s seconds ---" % (time.time() - start_time))

  # start_time = time.time()
  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  # print("4--- %s seconds ---" % (time.time() - start_time))

  # start_time = time.time()
  image = preprocess_input(image.copy())
  # print("5--- %s seconds ---" % (time.time() - start_time))

  # start_time = time.time()
  yhat = model.predict(image)
  # print("6--- %s seconds ---" % (time.time() - start_time))

  # start_time = time.time()
  label = decode_predictions(yhat)
  # print("7--- %s seconds ---" % (time.time() - start_time))

  label = label[0][0]
  print('%s (%.2f%%)' % (label[1], label[2]*100))
  return None

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
  
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat=0))

  channel = connection.channel()

  channel.queue_declare(queue='rpc_tensor_queue')


  channel.basic_qos(prefetch_count=1)
  # channel.queue_delete(queue='rpc_queue')
  channel.basic_consume(queue='rpc_tensor_queue', on_message_callback=on_request)

  print(" [x] Awaiting RPC requests")
  channel.start_consuming()
finally:
  pass
