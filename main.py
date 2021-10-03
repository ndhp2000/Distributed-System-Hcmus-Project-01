import logging
import sys

from Log.utils import get_custom_console_handler, get_custom_file_handler
from Network import signal_handler
from Network.network import Network


def init_log(iid):
    logger = logging.getLogger("__general_log__")
    logger.addHandler(get_custom_console_handler())
    logger.addHandler(get_custom_file_handler("./static/logs/{:02d}__console.log".format(iid)))

    logger = logging.getLogger("__sender_log__")
    logger.addHandler(get_custom_file_handler("./static/logs/{:02d}__sender.log".format(iid)))

    logger = logging.getLogger("__receiver_log__")
    logger.addHandler(get_custom_file_handler("./static/logs/{:02d}__receiver.log".format(iid)))


if __name__ == "__main__":
    n_instances = int(sys.argv[1])
    instance_id = int(sys.argv[2])
    signal_handler.register_exit_signal()
    init_log(instance_id)
    network = Network(instance_id, n_instances)
    try:
        network.start_sending()
        network.start_listening()
    except SystemExit:
        network.safety_closed()
