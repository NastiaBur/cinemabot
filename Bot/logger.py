import logging 


class LevelFilter(logging.Filter):

    def __init__(self, low, high):
        self._low = low
        self._high = high
        logging.Filter.__init__(self)

    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False
    
de_handler = logging.FileHandler('info.log', 'w')
de_handler.addFilter(LevelFilter(10, 30)) # info - warning
de_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

err_handler = logging.FileHandler('erros.log', 'w')
err_handler.addFilter(LevelFilter(40, 50)) # error - critical 
err_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))


bot_logger = logging.getLogger(name='cinemabot_logger')
bot_logger.setLevel(level=logging.DEBUG)
bot_logger.addHandler(de_handler)
bot_logger.addHandler(err_handler)

db_logger = logging.getLogger(name='database_logger')
db_logger.setLevel(level=logging.DEBUG)
db_logger.addHandler(de_handler)
db_logger.addHandler(err_handler)

kino_logger = logging.getLogger(name='kino_parse_logger')
kino_logger.setLevel(level=logging.DEBUG)
kino_logger.addHandler(de_handler)
kino_logger.addHandler(err_handler)

