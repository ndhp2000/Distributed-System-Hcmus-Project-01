import logging
import random
import threading

from constant import INT_SIZE, INT_REPR

logger = logging.getLogger("__receiver_log__")


class ReceiverWorker(threading.Thread):
    def __init__(self, connection, address, ses_clock):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.ses_clock = ses_clock
        self.shutdown_flag = threading.Event()
        self.noise = list()

    def run(self):
        while not self.shutdown_flag.is_set():
            data_size = int.from_bytes(self.connection.recv(INT_SIZE), INT_REPR, signed=True)
            if not data_size:
                break
            packet = self.connection.recv(data_size)
            self.noise.append(packet)
            if random.random() > 0.2 and len(self.noise):
                for packet in self.noise[::-1]:
                    self.ses_clock.deliver(packet)
                    logger.debug(
                        'RECEIVER #{}: Received message {} from {}:{}'.format(self.ident, packet, self.address[0],
                                                                              self.address[1]))
                self.noise.clear()

        self.connection.close()
        logger.warning('RECEIVER #{}: close connection to {}:{}'.format(self.ident, self.address[0], self.address[1]))
