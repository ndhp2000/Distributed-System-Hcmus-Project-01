import io
import logging
from threading import Semaphore

from .vector_clock import VectorClock

logger_send = logging.getLogger("__sender_log__")
logger_receive = logging.getLogger("__receiver_log__")


class SES:
    def __init__(self, n_instance, instance_id):
        self.vector_clock = VectorClock(n_instance, instance_id)
        self.queue = []
        self.lock = Semaphore(1)

    def __repr__(self):
        return repr(self.vector_clock) + "\n" + repr(self.queue)

    def __str__(self):
        return self.__repr__()

    def get_sender_log(self, destination_id, packet):
        string_stream = io.StringIO()
        print("Send Packet Info:", file=string_stream)
        print("\tSender ID: {}".format(self.vector_clock.instance_id), file=string_stream)
        print("\tReceiver ID: {}".format(destination_id), file=string_stream)
        print("\tPacket Content: {}".format(packet), file=string_stream)
        print("\tSender Clock:", file=string_stream)
        print("\t\tLocal logical clock:{}".format(self.vector_clock.get_clock(self.vector_clock.instance_id)),
              file=string_stream)
        print("\t\tLocal process vectors:", file=string_stream)
        for i in range(self.vector_clock.n_instance):
            if i != self.vector_clock.instance_id and not self.vector_clock.get_clock(i).is_null():
                print("\t\t\t<P_{}: {}>".format(i, self.vector_clock.get_clock(i)),
                      file=string_stream)
        return string_stream.getvalue()[:-1]

    def get_deliver_log(self, t_m, source_vector_clock, packet, status, header, print_compare):
        string_stream = io.StringIO()
        print("Received Packet Info {} :".format(header), file=string_stream)
        print("\tSender ID: {}".format(source_vector_clock.instance_id), file=string_stream)
        print("\tReceiver ID: {}".format(self.vector_clock.instance_id), file=string_stream)
        print("\tPacket Content: {}".format(packet), file=string_stream)
        #
        print("\tPacket Clock:", file=string_stream)
        print("\t\tt_m: {}".format(t_m),
              file=string_stream)
        print("\t\ttP_snd: {}".format(source_vector_clock.get_clock(source_vector_clock.instance_id)),
              file=string_stream)
        print("\tReceiver Logical Clock (tP_rcv):", file=string_stream)
        print("\t\t{}".format(self.vector_clock.get_clock(self.vector_clock.instance_id)),
              file=string_stream)
        print("\tStatus: {}".format(status), file=string_stream)
        if print_compare:
            print(
                "\tDelivery Condition:{} > {}".format(self.vector_clock.get_clock(self.vector_clock.instance_id), t_m),
                file=string_stream)
        return string_stream.getvalue()[:-1]

    def serialize(self, packet):
        """
        :param packet: bytes
        :return: packet with the vector_clock packed
        """
        return self.vector_clock.serialize(packet)

    def deserialize(self, packet):
        """
        :param packet: bytes
        :return: tuple (vector_clock: the vector clock, packet: left-over packet)
        """
        vector_clock, packet = self.vector_clock.deserialize(packet)
        return vector_clock, packet

    def merge(self, source_vector_clock):
        """
        :param source_vector_clock: merge vector clock in the received packet with the process clock.
        :return:
        """
        for i in range(self.vector_clock.n_instance):
            if i != self.vector_clock.instance_id and i != source_vector_clock.instance_id:
                self.vector_clock.merge(source_vector_clock, i, i)
        self.vector_clock.merge(source_vector_clock, source_vector_clock.instance_id, self.vector_clock.instance_id)
        self.vector_clock.increase()

    def deliver(self, packet):
        self.lock.acquire()  # synchronize
        source_vector_clock, packet = self.deserialize(packet)
        t_p = self.vector_clock.get_clock(self.vector_clock.instance_id)
        t_m = source_vector_clock.get_clock(self.vector_clock.instance_id)
        if t_m < t_p:
            # Deliver
            logger_receive.info(
                self.get_deliver_log(t_m, source_vector_clock, packet, status="delivering", header="BEFORE DELIVERED",
                                     print_compare=True))
            self.merge(source_vector_clock)
        else:
            # Queue
            self.queue.append((t_m, source_vector_clock, packet))
            logger_receive.info(
                self.get_deliver_log(t_m, source_vector_clock, packet, status="buffered", header="BEFORE BUFFERED",
                                     print_compare=True))
            break_flag = False
            while not break_flag:
                break_flag = True
                for index, (t_m, source_vector_clock, packet) in enumerate(self.queue):
                    if t_m < t_p:
                        logger_receive.info(
                            self.get_deliver_log(t_m, source_vector_clock, packet, status="delivering from buffer",
                                                 header="BEFORE DELIVERED FROM BUFFERED",
                                                 print_compare=True))
                        self.merge(source_vector_clock)
                        self.queue.pop(index)
                        break_flag = False
                        break
        self.lock.release()

    def send(self, destination_id, packet):
        self.lock.acquire()  # synchronize
        self.vector_clock.increase()
        logger_send.info(self.get_sender_log(destination_id, packet))
        result = self.serialize(packet)
        self.vector_clock.self_merge(self.vector_clock.instance_id, destination_id)
        self.lock.release()
        return result

# Module test
# p0 = SES(3, 0)
# p1 = SES(3, 1)
# p2 = SES(3, 2)
#
# print(p0)
# print(p1)
# print(p2)
# print('--------------')
#
# pk1 = p1.send(0, bytes("pk1", 'utf-8'))
# print(p1)
# print('--------------')
#
# pk2 = p1.send(0, bytes("pk2", 'utf-8'))
# print(p1)
# print('--------------')
#
# p0.deliver(pk2)
# print(p0)
# print('--------------')
# p0.deliver(pk1)
# print(p0)
# print('--------------')
#
# pk3 = p2.send(0, bytes("pk3", 'utf-8'))
# print(p2)
# print('--------------')
#
# pk4 = p2.send(1, bytes("pk4", 'utf-8'))
# print(p2)
# print('--------------')
#
# p1.deliver(pk4)
# print(p1)
# print('--------------')
#
# pk5 = p1.send(0, bytes("pk5", 'utf-8'))
# print(p1)
# print('--------------')
#
# p0.deliver(pk5)
# print(p0)
# print('--------------')
#
# p0.deliver(pk3)
# print(p0)
# print('--------------')


# send_packet = p1.send(0, bytes())
# print(p1.deserialize(send_packet))
# print(p1)
