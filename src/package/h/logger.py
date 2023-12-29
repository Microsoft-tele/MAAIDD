import logging


class SingletonLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(__name__)
            cls._instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(console_handler)
        return cls._instance
