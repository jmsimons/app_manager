import multiprocessing as mp
import traceback, sys


class AppManager:
    
    ''' Safely runs python application in child process '''

    def __init__(self, run_func, args = [], logger = None, run_limit = None):
        self.run_func = run_func
        self.logger = logger
        if run_limit and int(run_limit) > 0:
            self.run_limit = int(run_limit)
        else:
            self.run_limit = -1
        self.process = mp.Process(target = self.run_loop, args = (args, ))
        # # uncomment to start automatically after init #
        # self.start()
    
    def run_loop(self, proc_args):
        ''' runs in child process, contunially runs run_func, safely catches exceptions '''
        while True:
            # handle run_limit #
            if self.run_limit == 0:
                print("Run limit reached, stopping application")
                sys.exit()
            elif self.run_limit > 0:
                self.run_limit -= 1

            # run application #
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
        ''' starts the child process '''
        if run_limit and int(run_limit) > 0:
            self.run_limit = int(run_limit)
        message = "Starting application in AppManager"
        print(message)
        if self.logger:
            self.logger.info(message)
        self.process.start()

    def stop(self):
        ''' stops the child process '''
        message = "Stopping application"
        print(message)
        if self.logger:
            self.logger.info(message)
        self.process.terminate()