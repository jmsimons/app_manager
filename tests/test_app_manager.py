import unittest, time, logging
from multiprocessing import Manager, Value
from app_manager import AppManager


class SampleApp:
    ''' Sample application class for testing AppManager '''

    def __init__(self):
        self.running = Value('i', 0)
        self.logger = logging.getLogger()
        # TODO: Set up logger with file object to read from the test class
        
    def get_run_flag(self):
        return self.running
    
    def run(self, proc_args):
        run_tally, running = proc_args
        running.value = 1
        print("SampleApp sleeping for <1 second...")
        time.sleep(.99)
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
    def setUp(self):
        self.run_tally = Value('i', 0)
        self.app_man = AppManager(self.sample_app.run, args = [self.run_tally, self.sample_app.get_run_flag()])
    
    @classmethod
    def tearDown(self):
        if self.app_man.process.is_alive():
            self.app_man.process.terminate()

    def test_start(self):
        self.app_man.start()
        time.sleep(.25)
        self.assertEqual(self.sample_app.running.value, 1)
        time.sleep(3)
        self.assertGreater(self.run_tally.value, 1)

    def test_stop(self):
        self.app_man.start()
        time.sleep(.25)
        self.app_man.stop()
        time.sleep(.25)
        self.assertEqual(self.app_man.process.is_alive(), False)

    def test_run_limit(self):
        self.run_count = 0
        self.app_man.start(run_limit = 5)
        time.sleep(7) # long enough for the application to have run more than 5 times
        self.assertEqual(self.run_tally.value, 5)

    def test_logging(self):
        pass

if __name__ == "__main__":
    unittest.main()