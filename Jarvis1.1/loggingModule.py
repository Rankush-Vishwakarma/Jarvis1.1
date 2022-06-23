try:
    import logging
    import os
except Exception as e:
    print('Exception got in importing the module.')


class makeLog:
    def __init__(self):
        try:
            current_dir = os.getcwd()
            if 'log_files' in os.listdir(current_dir):
                path = os.path.join(current_dir, 'log_files\\')
                file_path = path + 'logfile.log'
                logging.basicConfig(filename=file_path,
                                    format='%(asctime)s %(message)s',
                                    filemode='w')
            else:
                path = os.path.join(current_dir, 'log_files\\')
                os.mkdir(path)
                file_path = path + 'logfile.log'
                logging.basicConfig(filename=file_path,
                                    format='%(asctime)s %(message)s',
                                    filemode='w')
    
            self.logger = logging.getLogger()
    
            self.logger.setLevel(logging.DEBUG)
        except Exception as e:
            print('Got Error in Logging module '+str(e))
            pass

    def debug(self, string):
        self.logger.debug(string)

    def info(self, string):
        self.logger.info(string)

    def warning(self, string):
        self.logger.warning(string)

    def error(self, string):
        self.logger.error(string)

    def critical(self, string):
        self.logger.critical(string)
