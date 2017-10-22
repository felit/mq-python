#coding:utf8
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.232.195'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
import time

t1 = time.time()
for i in range(1, 100000):
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!Hello World!Hello World!Hello World!')
t2 = time.time()
print('耗时:%sms' % (t2 - t1))
print(" [x] Sent 'Hello World!'")
connection.close()