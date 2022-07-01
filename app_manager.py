import multiprocessing as mp
import traceback, sys


class AppManager:
    
    ''' Runs python application in new process, safely catches exceptions and re-runs self.run_func '''

    def __init__(self, run_func, args = [], logger = None, run_limit = None):
        self.run_func = run_func
        self.logger = logger
        if run_limit and int(run_limit) > 0:
            self.run_limit = int(run_limit)
        else:
            self.run_limit = None
        self.process = mp.Process(target = self.run_loop, args = (args, ))
        # self.start() # uncomment to start automatically after init
    
    def run_loop(self, proc_args):
        while True:
            # handle run_limit #
            if self.run_limit == 0:
                print("Run limit reached, stopping application")
                sys.exit()
            elif self.run_limit > 0:
                self.run_limit -= 1

            # 
            try:
                if len(proc_args):
                    self.run_func(proc_args)
                else:
                    self.run_func()
            except:
                message = "Restarting after the following error..."
                print(message)
                traceback.print_exc()
                if self.logger:
                    self.logger.exception(message)

    def start(self, run_limit = None):
        if run_limit and int(run_limit) > 0:
            self.run_limit = int(run_limit)
        print("Starting application in AppManager")
        self.process.start()

    def stop(self):
        print("Stopping application")
        self.process.terminate()