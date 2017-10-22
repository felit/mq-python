# -*- coding:utf8 -*-
import pika
import unittest


class TestRabbitMQ(unittest.TestCase):
    def setUp(self):
        conn = pika.BlockingConnection()
        self.channel = conn.channel()
        self.large_number = 10

    def tearDown(self):
        print "do something after test.Clean up."
        pass

    def test_large_queue(self):
        for i in range(0, self.large_number):
            self.channel.queue_declare(durable=True, queue="queue%s" % str(i))

    def test_large_queue_delete(self):
        for i in range(0, self.large_number):
            self.channel.queue_delete("queue%s" % str(i))

    def test_large_exchange(self):
        for i in range(0, self.large_number):
            self.channel.exchange_declare(durable=True, exchange="exchange%s" % str(i), type='fanout')

    def test_large_exchange_delete(self):
        for i in range(0, self.large_number):
            self.channel.exchange_delete("exchange%s" % str(i))

    def test_fanout_exchange(self):
        self.channel.exchange_declare(exchange="exchange-fanout2", type='fanout', durable=True)
        self.channel.exchange_declare(exchange="exchange-fanout1", type='fanout', durable=True)

        self.channel.queue_declare(durable=True, queue="queue-fanout1")
        self.channel.queue_bind(exchange="exchange-fanout1", queue="queue-fanout1", routing_key="test")
        self.channel.queue_declare(durable=True, queue="queue-fanout2")
        self.channel.queue_bind(exchange="exchange-fanout1", queue="queue-fanout2", routing_key="test")
        self.channel.queue_declare(durable=True, queue="queue-fanout3")
        self.channel.queue_bind(exchange="exchange-fanout1", queue="queue-fanout3", routing_key="test")
        self.channel.queue_declare(durable=True, queue="queue-fanout4")
        self.channel.queue_bind(exchange="exchange-fanout1", queue="queue-fanout4", routing_key="test2")
        self.channel.queue_bind(exchange="exchange-fanout1", queue="queue-fanout4", routing_key="test3")
        # 绑定键的意义依赖于转发器的类型。对于fanout类型，忽略此参数
        self.channel.publish("exchange-fanout1", "tewst", "hello queue")

    def test_direct_exchange(self):
        self.channel.exchange_declare(exchange="exchange-direct", exchange_type='direct', durable=True)
        self.channel.queue_declare(queue="queue-direct1", durable=True)
        self.channel.queue_bind(exchange="exchange-direct", queue="queue-direct1", routing_key="test1")
        self.channel.queue_declare(queue="queue-direct2", durable=True)
        self.channel.queue_bind(exchange="exchange-direct", queue="queue-direct2", routing_key="test2")
        self.channel.queue_declare(queue="queue-direct3", durable=True)
        self.channel.queue_bind(exchange="exchange-direct", queue="queue-direct3", routing_key="test3")
        # 绑定两次会发两遍
        self.channel.queue_bind(exchange="exchange-direct", queue="queue-direct3", routing_key="test4")
        for i in range(0, 5):
            self.channel.publish("exchange-direct", "test%s" % (i), "hello queue%s" % i)

    def test_topic_exchange(self):
        self.channel.exchange_declare(exchange="exchange-topic", exchange_type="topic", durable=True)
        self.channel.queue_declare(queue="queue-topic1", durable=True)
        self.channel.queue_bind(exchange="exchange-topic", queue="queue-topic1", routing_key="test.1")

        self.channel.queue_declare(queue="queue-topic2", durable=True)
        self.channel.queue_bind(exchange="exchange-topic", queue="queue-topic2", routing_key="test.*")
        for i in range(0, 3):
            self.channel.publish("exchange-topic", "test.%s" % (i), "hello queue%s" % i)


if __name__ == '__main__':
    unittest.main()
    print dir(unittest)






