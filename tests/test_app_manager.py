import unittest, time, logging, os
from multiprocessing import Manager, Value
from app_manager.main import AppManager


class SampleApp:
    ''' Sample application class for testing AppManager '''

    def __init__(self):
        self.running = Value('i', 0)
        logging.basicConfig(filename = "sample_app.log", level = logging.INFO)
        self.logger = logging.getLogger()
    
    def run(self, proc_args):
        ''' runs in child process, sets status values, and throws exception '''
        run_tally, running = proc_args
        running.value = 1
        print("SampleApp sleeping for <1 second...")
        time.sleep(.99) # to give the test time to read running flag
        run_tally.value += 1
        running.value = 0
        # throw exception #
        1 / 0


class TestAppManager(unittest.TestCase):
    '''  '''

    @classmethod
    def setUpClass(self):
        self.sample_app = SampleApp()
    
    @classmethod
    def tearDownClass(self):
        if os.path.exists("sample_app.log"):
            os.remove("sample_app.log")
    
    @classmethod
    def setUp(self):
        self.run_tally = Value('i', 0)
        self.app_man = AppManager(
            self.sample_app.run,
            args = [self.run_tally, self.sample_app.running],
            logger = self.sample_app.logger)
    
    @classmethod
    def tearDown(self):
        if self.app_man.process.is_alive():
            self.app_man.process.terminate()

    def test_start(self):
        self.app_man.start()
        time.sleep(.5)
        self.assertEqual(self.sample_app.running.value, 1)

    def test_stop(self):
        self.app_man.start()
        time.sleep(.5)
        self.app_man.stop()
        time.sleep(.1)
        self.assertEqual(self.app_man.process.is_alive(), False)

    def test_run_limit(self):
        self.run_count = 0
        self.app_man.start(run_limit = 5)
        time.sleep(7) # long enough for the application to run more than 5 times
        self.assertEqual(self.run_tally.value, 5)

    def test_logging(self):
        self.app_man.start()
        time.sleep(.1)
        self.app_man.stop()
        time.sleep(.1)
        log_file = open("sample_app.log").read()
        self.assertGreater(len(log_file), 0)
