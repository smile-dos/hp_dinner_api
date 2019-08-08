from kombu import Connection, Producer, Consumer, Queue, uuid
from core import settings
import pickle


class RpcProxy(object):

    def __init__(self, amqp_url):
        self.connection = Connection(amqp_url)
        self.callback_queue = Queue(uuid(), exclusive=True, auto_delete=True)

    def on_response(self, message):
        if message.properties['correlation_id'] == self.correlation_id:
            result = message.payload
            ret = pickle.loads(result)
            if isinstance(ret, Exception):
                raise ret
            else:
                self.response = ret

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self.response = None
            self.correlation_id = uuid()
            with Producer(self.connection) as producer:
                producer.publish(
                    pickle.dumps((name, args, kwargs)),
                    exchange='',
                    routing_key=settings.RPC_QUEUE,
                    declare=[self.callback_queue],
                    reply_to=self.callback_queue.name,
                    correlation_id=self.correlation_id,
                )

            with Consumer(
                    self.connection,
                    on_message=self.on_response,
                    queues=[self.callback_queue],
                    no_ack=True,
                    accept=['json', 'pickle', 'msgpack']):
                while self.response is None:
                    self.connection.drain_events()
            return self.response

        return do_rpc


rpc_proxy = RpcProxy(settings.RPC_BROKER_URL)
