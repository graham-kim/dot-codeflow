import typing as tp
import unittest
import inspect
from pathlib import Path

from entities.dotClass import DotClass
from entities.dotFunction import DotFunction

expectations_dir = Path("entities/tests/expectations/")

class TestDotClass(unittest.TestCase):
    def check_expectations(self, c: DotClass) -> None:
        caller_name = inspect.stack()[1].function
        with open(expectations_dir / f'{caller_name}.txt', 'r') as expF:
            self.assertEqual(str(c), expF.read())

    def update_expectations(self, c: DotClass) -> None:
        caller_name = inspect.stack()[1].function
        with open(expectations_dir / f'{caller_name}.txt', 'w') as expF:
            expF.write(str(c))

    def test_empty_class(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        self.check_expectations(c)

        self.assertTrue(c.empty(), msg="DotClass should be empty with nothing added")

    def test_class_with_member_variables(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        c.add_member_variable("count", "int", 15)
        c.add_member_variable("name", "const char *", 16)
        self.check_expectations(c)
        
        d = DotClass("SomeActor", "path/to/actor.cc", 146)
        d.add_member_variable("count", line_num=15, var_type="int")
        d.add_member_variable("name", "std::string", 16, label="const char * name")
        self.check_expectations(d)

        self.assertFalse(c.empty(), msg="DotClass should not be empty as something was added")

    def test_class_with_methods(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        f1 = DotFunction("doSomething", 30, label="Namespace::doSomething()")
        f2 = DotFunction("incrCount", 31)
        f2.add_param("count", "int")
        c.add_method(f1)
        c.add_method(f2)
        self.check_expectations(c)

        self.assertFalse(c.empty(), msg="DotClass should not be empty as something was added")

    def test_class_with_method_needing_escapes(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        f1 = DotFunction("doSomething", 30, label="Namespace::[[B]]do[[/B]]Something\\n<B>()")
        c.add_method(f1)
        self.check_expectations(c)

    def test_class_with_colon_in_name(self) -> None:
        c = DotClass("Entity::SomeActor", "path/to/actor.cc", 146)
        c.add_member_variable("count", "int", 15)
        f = DotFunction("doSomething", 30, label="Namespace::doSomething()")
        c.add_method(f)
        self.check_expectations(c)

    def test_class_with_method_having_local_var(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        f = DotFunction("doSomething", 30, label="Namespace::[[B]]do[[/B]]Something\\n<B>()")
        f.add_param("count", "int")
        f.add_local_var("sum", "int")
        c.add_method(f)
        self.check_expectations(c)

    def test_class_with_method_having_loop(self) -> None:
        c = DotClass("SomeActor", "path/to/actor.cc", 146)
        f = DotFunction("doSomething", 30, retval="bool", label="Namespace::[[B]]do[[/B]]Something\\n<B>()")
        f.add_param("count", "int")
        f.add_loop("while", 34)
        c.add_method(f)
        self.check_expectations(c)