INT_SIZE = 4
INT_REPR = 'big'


class LogicClock:
    def __init__(self, n_instance, instance_id, zero_fill=False):
        self.n_instance = n_instance
        self.instance_id = instance_id
        self._clock = [-1] * n_instance
        if zero_fill:
            self._clock = [0] * n_instance

    def __repr__(self):
        return str(self.get_time())

    def __str__(self):
        return self.__repr__()

    def __gt__(self, other):
        for i in range(self.n_instance):
            if self._clock[i] <= other.get_time()[i]:
                return False
        return True

    def __ge__(self, other):
        for i in range(self.n_instance):
            if self._clock[i] < other.get_time()[i]:
                return False
        return True

    def serialize(self):
        data = bytes()
        for i in range(self.n_instance):
            data = data + self._clock[i].to_bytes(INT_SIZE, INT_REPR, signed=True)
        return data

    def deserialize(self, data):
        new_clock = LogicClock(self.n_instance, self.instance_id)
        for i in range(self.n_instance):
            new_clock._clock[i] = int.from_bytes(data[INT_SIZE * i: INT_SIZE * (i + 1)], INT_REPR, signed=True)
        return new_clock

    def get_time(self):
        return tuple(self._clock)

    def increase(self):
        self._clock[self.instance_id] += 1

    def is_null(self):
        for i in range(self.n_instance):
            if self._clock[i] == -1:
                return True
        return False

    def merge(self, other):
        if self.is_null():
            for i in range(self.n_instance):
                self._clock[i] = other.get_time()[i]
        else:
            for i in range(self.n_instance):
                self._clock[i] = max(self._clock[i], other.get_time()[i])

# clock = LogicClock(3, 0)
# print(clock.get_time())
# clock.increase()
# print(clock.get_time())
