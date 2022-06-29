import multiprocessing as mp
import sys, traceback


class AppManager:
    
    ''' Runs python application in new process, safely catches exceptions and re-runs self.run_func '''

    def __init__(self, run_func, logger = None):
        self.run_func = run_func
        self.logger = logger
        self.process = mp.Process(target = self.start)
        self.process.start()
    
    def start(self):
        while True:
            try:
                self.run_func()
            except:
                message = "Restarting after the following error..."
                print(message)
                traceback.print_exe()
                if self.logger:
                    self.logger.exception(message)
