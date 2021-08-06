import unittest
from stocklab.agent.ebest import EBest
import inspect
import time

class TestEbest(unittest.TestCase):
    def setUp(self):
        self.ebest = EBest("DEMO")
        self.ebest.login()
    
    def tearDown(self):
        self.ebest.logout()
        self.ebest.logout()