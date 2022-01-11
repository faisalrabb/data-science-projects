import unittest
from pathlib import Path
import os, sys
import json, csv
from src.compile_word_counts import get_speech_frequency
from src.compute_pony_lang import get_stats
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...
        response = get_speech_frequency(self.mock_dialog)
        with open(self.true_word_counts, 'r') as t:
            f = json.load(t)
        self.assertTrue(f ==response)
    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        response = get_stats(self.true_word_counts, 2)
        with open(self.true_tf_idfs, 'r') as t:
            f = t.read()
        self.assertTrue(f.strip() ==response.strip())
        
    
if __name__ == '__main__':
    unittest.main()