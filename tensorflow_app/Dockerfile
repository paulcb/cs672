FROM tensorflow/tensorflow
RUN apt -y update
# RUN apt -y install rabbitmq-server
# RUN service rabbitmq-server start

RUN apt -y install python3
RUN apt -y install python3-pip
RUN pip3 install pillow
RUN pip3 install pika
COPY ../vgg16_2.py /opt
COPY ../rpc_server_tensorflow.py /opt
COPY ../elephant.jpg /opt
RUN python3 /opt/vgg16_2.py /opt/elephant.jpg
CMD ["python3", "/opt/rpc_server_tensorflow.py", "rabbit-0", "sleep"]
# RUN python3 /opt/rpc_server.py
