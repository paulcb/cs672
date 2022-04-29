FROM ubuntu
RUN apt -y update
# RUN apt -y install rabbitmq-server
# RUN service rabbitmq-server start

RUN apt -y install python3
RUN apt -y install python3-pip
RUN apt -y install sysstat
RUN pip3 install pillow
RUN pip3 install pika
RUN pip3 install psutil
COPY rpc_server.py /opt
COPY rpc_client.py /opt
COPY app_a_cmd.sh /opt
CMD ["python3", "/opt/rpc_server.py", "rabbit-0", "sleep"]
# CMD ["/opt/app_a_cmd.sh"]
# RUN python3 /opt/rpc_server.py
