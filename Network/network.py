import logging
import socket

from SES.ses import SES
from constant import PORT_OFFSET
from .receiver import ReceiverWorker
from .sender import SenderWorker

logger = logging.getLogger("__general_log__")


class Network:
    ip = '127.0.0.1'

    def __init__(self, instance_id, n_instances):
        self.instance_id = instance_id
        self.n_instances = n_instances
        self.port = PORT_OFFSET + instance_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.sender_list = []
        self.receiver_list = []
        self.ses_clock = SES(n_instances, instance_id)

    def start_listening(self):
        self.socket.listen()
        logger.info("Server is Listening on {}:{}".format(self.ip, self.port))
        while True:
            connection, address = self.socket.accept()
            logger.info('Open Connection with {}:{}'.format(address[0], address[1]))
            receiver = ReceiverWorker(connection, address, self.ses_clock)
            receiver.start()
            self.receiver_list.append(receiver)

    def start_sending(self):
        for instance_id in range(self.n_instances):
            if self.instance_id == instance_id:
                continue
            sender = SenderWorker(self.instance_id, instance_id, self.ip, PORT_OFFSET + instance_id, self.ses_clock)
            sender.start()
            self.sender_list.append(sender)

    def safety_closed(self):
        self.socket.close()
        logger.warning('Force to stop. Cleaning all children processes.')
        for sender in self.sender_list:
            sender.shutdown_flag.set()
        for receiver in self.receiver_list:
            receiver.shutdown_flag.set()
