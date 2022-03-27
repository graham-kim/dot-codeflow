import typing as tp
import unittest
import inspect
from pathlib import Path

from parsers.node import NodeParser

inputs_dir = Path("parsers/tests/inputs/")

class TestNodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = NodeParser()

    def parse_test_input(self) -> None:
        caller_name = inspect.stack()[1].function
        self.parser.parse_file(inputs_dir / f'{caller_name}.txt')

    def test_parse_two_classes(self) -> None:
        self.parse_test_input()

        self.assertEqual(2, len(self.parser.finished_classes), msg= \
            "Should have parsed correct number of classes")

        class0 = self.parser.finished_classes[0]
        self.assertEqual(2, len(class0.member_variables), msg= \
            "First class should have expected number of member variables")
        self.assertEqual(2, len(class0.methods), msg= \
            "First class should have expected number of methods")
        self.assertEqual(1, len(class0.methods[0].params), msg= \
            "First method of first class should have expected number of params")

        class1 = self.parser.finished_classes[1]
        self.assertEqual(3, len(class1.member_variables), msg= \
            "Second class should have expected number of member variables")

    def test_bad_param_line(self) -> None:
        with self.assertRaises(Exception) as ex:
            self.parse_test_input()
        self.assertTrue("Expected a function to parse this line under" in str(ex.exception), \
            msg=f"Exception message does not explain problem:\n  {ex.exception}")

    def test_method_without_class(self) -> None:
        with self.assertRaises(Exception) as ex:
            self.parse_test_input()
        self.assertTrue("Expected a class to parse this line under" in str(ex.exception), \
            msg=f"Exception message does not explain problem:\n  {ex.exception}")

    def test_class_broken_by_comment(self) -> None:
        with self.assertRaises(Exception) as ex:
            self.parse_test_input()
        self.assertTrue("Expected a class to parse this line under" in str(ex.exception), \
            msg=f"Exception message does not explain problem:\n  {ex.exception}")