import typing as tp
import unittest
import inspect
from pathlib import Path

from entities.dotClass import DotClass

expectations_dir = Path("entities/tests/expectations/")

class TestDotClass(unittest.TestCase):
    def check_expectations(self, c: DotClass) -> None:
        caller_name = inspect.stack()[1].function
        with open(expectations_dir / f'{caller_name}.txt', 'r') as expF:
            self.assertTrue(str(c), expF.read())

    def update_expectations(self, c: DotClass) -> None:
        caller_name = inspect.stack()[1].function
        with open(expectations_dir / f'{caller_name}.txt', 'w') as expF:
            expF.write(str(c))

    def test_empty_class(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        self.check_expectations(c)

    def test_class_with_member_variables(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        c.add_member_variable("count", 15, "int")
        c.add_member_variable("name", 16, "const char *")
        self.check_expectations(c)
        
        d = DotClass("SomeActor", "path/to/actor.cc", 146)
        d.add_member_variable("count", line_num=15, var_type="int")
        d.add_member_variable("name", 16, label="const char * name")
        self.check_expectations(d)