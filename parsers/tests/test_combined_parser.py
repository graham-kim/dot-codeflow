import typing as tp
import unittest
import inspect
from pathlib import Path

from parsers.combined import CombinedParser

inputs_dir = Path("parsers/tests/inputs/combined_parser/")

class TestCombinedParser(unittest.TestCase):
    def setUp(self):
        self.parser = CombinedParser()

    def parse_test_input(self) -> None:
        caller_name = inspect.stack()[1].function
        self.parser.parse_file(inputs_dir / f'{caller_name}.txt')

    def test_parse_two_classes_no_links(self) -> None:
        self.parse_test_input()

        finished_classes = self.parser.node_parser.finished_classes
        self.assertEqual(2, len(finished_classes), msg= \
            "Should have parsed correct number of classes")

        class0 = finished_classes["SomeActor"]
        self.assertEqual(2, len(class0.member_variables), msg= \
            "First class should have expected number of member variables")
        self.assertEqual(2, len(class0.methods), msg= \
            "First class should have expected number of methods")
        self.assertEqual(1, len(class0.methods[0].params), msg= \
            "First method of first class should have expected number of params")

        class1 = finished_classes["GreatStruct"]
        self.assertEqual(3, len(class1.member_variables), msg= \
            "Second class should have expected number of member variables")

    def test_parse_two_classes_with_links(self) -> None:
        self.parse_test_input()

        finished_classes = self.parser.node_parser.finished_classes
        self.assertEqual(2, len(finished_classes), msg= \
            "Should have parsed correct number of classes")

        finished_links = self.parser.link_parser.finished_links
        self.assertEqual(2, len(finished_links), msg= \
            "Should have parsed correct number of links")

        self.assertEqual("SomeActor_ctor -> GreatStruct_calculateSomething", \
            str(finished_links[0]).strip(), msg= "Should have parsed link correctly")
        self.assertEqual("GreatStruct_calculateSomething -> SomeActor_mem_var:isValid [style=dotted]", \
            str(finished_links[1]).strip(), msg= "Should have parsed link correctly")

    def test_new_file_adding_new_class_and_links(self) -> None:
        self.parser.parse_file(inputs_dir / 'test_parse_two_classes_with_links.txt')
        self.parse_test_input()

        finished_classes = self.parser.node_parser.finished_classes
        self.assertEqual(3, len(finished_classes), msg= \
            "Should have parsed correct number of classes")

        finished_links = self.parser.link_parser.finished_links
        self.assertEqual(4, len(finished_links), msg= \
            "Should have parsed correct number of links")

        link_heads = [str(l).split('->')[0].strip() for l in finished_links]
        self.assertEqual(3, link_heads.count("SomeActor_ctor"), msg= \
            "Should have parsed correct number of links which start from this node")

    def test_new_file_adding_new_methods_to_existing_class(self) -> None:
        self.parser.parse_file(inputs_dir / 'test_parse_two_classes_with_links.txt')
        self.parse_test_input()

        finished_links = self.parser.link_parser.finished_links
        self.assertEqual(4, len(finished_links), msg= \
            "Should have parsed correct number of links")

        link_tails = [str(l).split('->')[1].strip() for l in finished_links]
        self.assertEqual(2, link_tails.count("SomeActor_incrCount [style=dashed color=red]"), msg= \
            "Should have parsed correct number of links which end on this node")
