import typing as tp
import unittest
import inspect
from pathlib import Path

from parsers.link import LinkParser

inputs_dir = Path("parsers/tests/inputs/link_parser/")

class TestLinkParser(unittest.TestCase):
    def setUp(self):
        self.parser = LinkParser()

    def parse_test_input(self) -> None:
        caller_name = inspect.stack()[1].function
        self.parser.parse_file(inputs_dir / f'{caller_name}.txt')

    def test_parse_three_links(self) -> None:
        self.parse_test_input()

        self.assertEqual(3, len(self.parser.finished_links), msg= \
            "Should have parsed expected number of links")
        self.assertEqual("abc:call", self.parser.finished_links[0].src, msg= \
            "First link should have put : in the src")
        self.assertEqual("more label text", self.parser.finished_links[1].label, msg= \
            "Second link should have separated the label from the tags")

    def test_incomplete_link(self) -> None:
        with self.assertRaises(Exception) as ex:
            self.parse_test_input()
        self.assertTrue("Incomplete link detected" in str(ex.exception), msg= \
            "Exception message does not describe problem")

    def test_parse_colon_in_link(self) -> None:
        self.parse_test_input()

        self.assertEqual(1, len(self.parser.finished_links), msg= \
            "Should have parsed expected number of links")
        self.assertEqual("abc__vda:call", self.parser.finished_links[0].src, msg= \
            "First link should have replaced : for _ and then put : for the port in the src")
