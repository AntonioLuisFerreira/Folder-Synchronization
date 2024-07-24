import logging

class LogConfiguration:

    def config(log_path: str):
        """ Does a basic configuration of the log file
            Parameters:
                log_path: path to the log file
        """
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')