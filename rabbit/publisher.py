import pika
import json


class Publisher(object):
    EXCHANGE = 'message'
    EXCHANGE_TYPE = 'direct'
    PUBLISH_INTERVAL = 1

    def __init__(self, amqp_url, queue, routing_key, article_urls):
        self._connection = None
        self._channel = None
        self._deliveries = []
        self._message_number = 0
        self._stopping = False
        self._url = amqp_url
        self._queue = queue
        self._article_urls = article_urls
        self._routing_key = routing_key
        self._closing = False

    def connect(self):
        return pika.SelectConnection(
            pika.URLParameters(self._url),
            self.on_connection_open,
            stop_ioloop_on_close=False)

    def close_connection(self):
        self._closing = True
        self._connection.close()

    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self._connection.add_timeout(5, self.reconnect)

    def on_connection_open(self, unused_connection):
        self.add_on_connection_close_callback()
        self.open_channel()

    def reconnect(self):
        self._connection.ioloop.stop()
        self._connection = self.connect()
        self._connection.ioloop.start()

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        if not self._closing:
            self._connection.close()

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def setup_exchange(self, exchange_name):
        self._channel.exchange_declare(
            self.on_exchange_declareok,
            exchange_name,
            self.EXCHANGE_TYPE)

    def on_exchange_declareok(self, unused_frame):
        self.setup_queue(self._queue)

    def setup_queue(self, queue_name):
        self._channel.queue_declare(self.on_queue_declareok, queue_name)

    def on_queue_declareok(self, method_frame):
        self._channel.queue_bind(
            self.on_bindok,
            self._queue,
            self.EXCHANGE,
            self._routing_key)

    def on_delivery_confirmation(self, method_frame):
        self._deliveries.remove(method_frame.method.delivery_tag)

    def enable_delivery_confirmations(self):
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def publish_message(self):
        if self._stopping:
            return

        message = json.dumps({
            'url': self._article_urls.pop()
        })

        self._channel.basic_publish(
            self.EXCHANGE,
            self._routing_key,
            message)
        self._message_number += 1
        self._deliveries.append(self._message_number)
        self.schedule_next_message()

    def schedule_next_message(self):
        if self._stopping:
            return
        self._connection.add_timeout(self.PUBLISH_INTERVAL, self.publish_message)

    def start_publishing(self):
        self.enable_delivery_confirmations()
        self.schedule_next_message()

    def on_bindok(self, unused_frame):
        self.start_publishing()

    def close_channel(self):
        if self._channel:
            self._channel.close()

    def open_channel(self):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        self._stopping = True
        self.close_channel()
        self.close_connection()
        self._connection.ioloop.start()
