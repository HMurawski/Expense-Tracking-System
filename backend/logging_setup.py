import logging

def setup_logger(name, log_file="server.log", level=logging.DEBUG):
    #creating custom logger
    logger = logging.getLogger(name)
    
    #config
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger