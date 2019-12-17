import logging
from logging.handlers import RotatingFileHandler
import getpass


def log_msg(log_file, script, msg):
    """
    Send logging to ``.netor/log/log_file`` file the message adding userID who executed the task.


    :param log_file: logging file name
    :param script: script name who is sending the message to log
    :param msg: message to store
    :return: nothing
    """

    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logger = logging.getLogger(__name__)

    logger.setLevel('DEBUG')

    formatter = logging.Formatter(log_format)

    size_handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)

    size_handler.setFormatter(formatter)

    logger.addHandler(size_handler)

    logger.info(msg + " - by: " + getpass.getuser() + " at script: " + script)


def _main():
    pass


if __name__ == '__main__':
    _main()
    print()
