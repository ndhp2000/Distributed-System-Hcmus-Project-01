import logging
import random
import socket
import threading
import time

INT_SIZE = 4
INT_REPR = 'big'
logger = logging.getLogger("__sender_log__")


class SenderWorker(threading.Thread):
    def __init__(self, instance_id, destination_id, ip, port, ses_clock):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.ses_clock = ses_clock
        self.instance_id = instance_id
        self.destination_id = destination_id
        self.message_count = 0
        self.shutdown_flag = threading.Event()

    def run(self):
        logger.info('SENDER #{}: started'.format(self.ident))
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not self.shutdown_flag.is_set():
            try:
                logger.info('SENDER #{}: create sender connect to {}:{}'.format(self.ident, self.ip, self.port))
                sender.connect((self.ip, self.port))
                break
            except ConnectionRefusedError:
                logger.warning(
                    'SENDER #{}: connection to {}:{} failed, retry after 500 milliseconds.'.format(self.ident, self.ip,
                                                                                                   self.port))
                time.sleep(0.5)

        while not self.shutdown_flag.is_set():
            try:
                self.message_count = self.message_count + 1
                message = bytes("Message from {}, number {}".format(self.instance_id, self.message_count), 'utf-8')
                message = self.ses_clock.send(self.destination_id, message)
                data_size = len(message)
                message = data_size.to_bytes(INT_SIZE, INT_REPR, signed=True) + message
                sender.send(message)
                logger.debug('SENDER #{}: send message {} to {}:{}'.format(self.ident, message, self.ip, self.port))
                time.sleep(random.random())
            except BrokenPipeError:
                break
        sender.close()
        logger.warning('SENDER #{}: Close connection to {}:{}'.format(self.ident, self.ip, self.port))
