import unittest
from pipeline import Pipeline
from configuration import cfg
pipeline = Pipeline(cfg)

class TestStringMethods(unittest.TestCase):

    def test_pipeline_special_chars(self):
        self.assertEqual(len(pipeline("La france entière et le chômage", format='json')["ents"]), 2)
        self.assertEqual(len(pipeline("La france entière et le chomage", format='json')["ents"]), 2)

if __name__ == '__main__':
    unittest.main()