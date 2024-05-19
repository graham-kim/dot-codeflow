import typing as tp
import unittest

from parsers.shorthand import ShorthandParser

class TestShortFlow(unittest.TestCase):
#    @classmethod
#    def setUpClass(cls):
#        self.cat_dict = {
#            "x": 'fillcolor="#FF9999"',
#            "o": 'fillcolor="#55FF55"'
#        }

    def setUp(self):
        self.parser = ShorthandParser()

    def test_single_chain(self):
        filename = "tests/shortflow_files/single_chain.txt"
        self.parser.parse_file(filename)

        self.assertTrue( len(self.parser.node_dict) == 3, \
            f"Expected exactly 3 nodes: {self.parser}")
        def check_individual_name(node_name):
            self.assertTrue( node_name in self.parser.node_dict, \
                f"Expected node name {node_name} in {self.parser.node_dict}")
        for node_name in ["ABC", "DEF", "GHI"]:
            check_individual_name(node_name)
        
        filtered_lines = list(filter(len, self.parser.link_lines))
        self.assertTrue( len(filtered_lines) == 3, \
            f"Expected exactly 3 link lines: {filtered_lines}")

