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

    def check_individual_name(self, node_name: str):
        self.assertTrue( node_name in self.parser.node_dict, \
            f"Expected node name {node_name} in {self.parser.node_dict}")

    def test_single_chain(self):
        filename = "tests/shortflow_files/single_chain.txt"
        self.parser.parse_file(filename)

        self.assertTrue( len(self.parser.node_dict) == 3, \
            f"Expected exactly 3 nodes: {self.parser}")

        for node_name in ["ABC", "DEF", "GHI"]:
            self.check_individual_name(node_name)
        
        filtered_lines = list(filter(len, self.parser.link_lines))
        self.assertTrue( len(filtered_lines) == 3, \
            f"Expected exactly 3 link lines: {filtered_lines}")

    def test_repeat_nodes(self):
        filename = "tests/shortflow_files/repeat_nodes.txt"
        self.parser.parse_file(filename)

        for node_name in ["ABC", "DEF", "GHI", "JKL"]:
            self.check_individual_name(node_name)

        def get_node_label(node_name) -> str:
            if self.parser.node_dict[node_name].label is None:
                return ""
            return " ".join(self.parser.node_dict[node_name].label.asList())

        self.assertTrue( get_node_label("ABC") == "the abc node", \
            f"Expected the ABC node's label to be its first value: {get_node_label('ABC')}")
        self.assertTrue( get_node_label("JKL") == "", \
            f"Expected the JKL node's label to be blank, its first value: {get_node_label('JKL')}")

