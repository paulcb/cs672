FROM ubuntu
RUN apt -y update
# RUN apt -y install rabbitmq-server
# RUN service rabbitmq-server start

RUN apt -y install python3
RUN apt -y install python3-pip
RUN pip3 install pillow
RUN pip3 install pika
COPY ../rpc_server.py /opt
COPY ../rpc_client.py /opt

CMD ["python3", "/opt/rpc_server.py", "rabbit-0"]
# RUN python3 /opt/rpc_server.py
