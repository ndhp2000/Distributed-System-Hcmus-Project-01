import logging

logging.root.setLevel(logging.NOTSET)


def get_custom_console_handler():
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(name)s - %(levelname)s: \n%(message)s\n--------------------')
    c_handler.setFormatter(c_format)
    return c_handler


def get_custom_file_handler(directory):
    f_handler = logging.FileHandler(directory)
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: \n%(message)s\n---------------------')
    f_handler.setFormatter(f_format)
    return f_handler
