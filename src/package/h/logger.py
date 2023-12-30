import logging

import src.package.h.config as h


class SingletonLogger:
    _instance = None

    def __new__(cls, config: h.ProjectPath):
        if not cls._instance:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(__name__)
            cls._instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s')

            if h.is_show_log:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                cls._instance.logger.addHandler(console_handler)

            file_handler = logging.FileHandler(config.get_log_save_path())
            file_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(file_handler)
        return cls._instance
