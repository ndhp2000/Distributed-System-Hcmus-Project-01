from .clock import LogicClock

INT_SIZE = 4
INT_REPR = 'big'


class VectorClock:
    def __init__(self, n_instance, instance_id):
        self.instance_id = instance_id
        self.n_instance = n_instance
        self.vectors = []
        for i in range(n_instance):
            self.vectors.append(LogicClock(n_instance, i, i == instance_id))

    def __repr__(self):
        result = "({},{})".format(self.n_instance, self.instance_id)
        for i in range(self.n_instance):
            result += "\n{}".format(self.vectors[i])
        return result

    def __str__(self):
        return self.__repr__()

    def serialize(self, packet):
        data = bytes()
        data = data + self.instance_id.to_bytes(INT_SIZE, INT_REPR)
        for i in range(self.n_instance):
            data = data + self.vectors[i].serialize()
        return data + packet

    def deserialize(self, packet):
        data_size = INT_SIZE * (self.n_instance * self.n_instance + 1)
        data, packet = packet[0:data_size], packet[data_size:]

        new_instance_id = int.from_bytes(data[0:INT_SIZE], INT_REPR, signed=True)
        new_vector_clock = VectorClock(self.n_instance, new_instance_id)
        data = data[INT_SIZE:]

        for i in range(self.n_instance):
            new_vector_clock.vectors[i] = new_vector_clock.vectors[i].deserialize(
                data[INT_SIZE * self.n_instance * i: INT_SIZE * self.n_instance * (i + 1)])

        return new_vector_clock, packet

    def increase(self):
        self.vectors[self.instance_id].increase()

    def self_merge(self, source_id, destination_id):
        """
        Merge P_source_id to P_destination_id
        :param source_id:
        :param destination_id:
        """
        self.vectors[destination_id].merge(self.vectors[source_id])

    def merge(self, source_vector_clock, source_id, destination_id):
        """
        Merge P_source_id from the source vector clock to P_destination_id
        :param source_vector_clock:
        :param source_id:
        :param destination_id:
        :return:
        """
        self.vectors[destination_id].merge(source_vector_clock.vectors[source_id])

    def get_clock(self, index):
        return self.vectors[index]

# def Testing():
#     for n in range(2, 100):
#         k = random.randint(0, n - 1)
#         vc1 = VectorClock(n, k)
#         for i in range(n):
#             for j in range(n):
#                 vc1.vectors[i]._clock[j] = random.randint(0, 1000) - 500
#         temp = vc1.serialize(bytes())
#         A = vc1.deserialize(temp)[0].vectors
#         B = vc1.vectors
#         assert (str(A) == str(B))


# print(random.randint(0, n - 1))
# for i in range(1000):
#     Testing()
#     print("Runnint test {} success.".format(i))
# vc1 = VectorClock(2, 0)
# vc1.vectors[0]._clock[1] = 1000
# print("INPUT\n", vc1)
# temp = vc1.serialize(bytes())
# A = vc1.deserialize(temp)[0].vectors
# B = vc1.vectors
# print(A)
# print(B)
# print("OUTPUT:\n", str(A) == str(B))
