import logging

class LoggingInit():
    @property
    def logger(self):
        return self._logger

    def __init__(self, level=logging.DEBUG, msg_format= '%(asctime)s %(levelname)s %(name)s: %(message)s', date_format= '%Y-%m-%d %H:%M:%S') -> None:
        self.msg_format = msg_format
        self.date_format = date_format
        self.level = level            
        self._logger=self.set_logging()
        pass
    
    def set_logging(self):
        logging.basicConfig(format=self.msg_format, datefmt=self.date_format, stream=sys.stdout)
        logger = logging.getLogger()        
        logger.setLevel(self.level)
        logger.info("Logger Initializated")
        return (logger)