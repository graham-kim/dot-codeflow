import typing as tp
from entities.dotClass import DotClass
from entities.dotFunction import DotFunction

class NodeParser:
    def __init__(self):
        self.current_class: DotClass = None
        self.current_function: DotFunction = None
        self.finished_classes: tp.List[DotClass] = []
        self.standalone_functions: tp.List[DotFunction] = []

    def _finish_class(self) -> None:
        if self.current_class and not self.current_class.empty():
            self.finished_classes.append(self.current_class)
        self.current_class = None
        self.current_function = None

    def _check_current_class_exists(self, line: str) -> None:
        if self.current_class is None:
            raise Exception(f"Expected a class to parse this line under:\n{line}")

    def _check_current_function_exists(self, line: str) -> None:
        if self.current_function is None:
            raise Exception(f"Expected a function to parse this line under:\n{line}")

    def _start_class(self, line: str) -> None:
        tokens = line.split(' ')
        if len(tokens) < 2 or len(tokens) > 3:
            raise Exception(f"Wrong number of tokens when starting a class:\n{line}")

        num: int = None
        if len(tokens) == 3:
            num = int(tokens[2].strip())

        self.current_class = DotClass(name=tokens[0].strip(), filepath=tokens[1].strip(), line_num=num)

    def _parse_member_variable(self, line: str) -> None:
        original_line = line
        label: str = None
        if '|' in line:
            label_tokens = line.split('|')
            label = label_tokens[1].strip()
            line = label_tokens[0].strip()

        tokens = line[2:].split(' ')
        if len(tokens) < 1 or len(tokens) > 3:
            raise Exception(f"Wrong number of tokens when parsing a member variable:\n{original_line}")

        var_type: str = None
        if len(tokens) > 1:
            var_type = tokens[1].strip()

        num: int = None
        if len(tokens) == 3:
            num = int(tokens[2].strip())

        self.current_class.add_member_variable( \
            name=tokens[0].strip(), var_type=var_type, line_num=num, label=label)

    def _parse_method(self, line: str) -> None:
        original_line = line
        label: str = None
        if '|' in line:
            label_tokens = line.split('|')
            label = label_tokens[1].strip()
            line = label_tokens[0].strip()

        retval: str = None
        if '@' in line:
            ret_tokens = line.split('@')
            retval = ret_tokens[1].strip()
            line = ret_tokens[0].strip()

        tokens = line[2:].split(' ')
        if len(tokens) < 2 or len(tokens) > 3:
            raise Exception(f"Wrong number of tokens when parsing a member variable:\n{original_line}")

        name = tokens[0].strip()
        if not label and len(tokens) == 3:
            src_filename = tokens[1].strip()
            if src_filename:
                label = f"{name}()\\n{src_filename}"
        self.current_function = DotFunction( \
            name=name, line_num=tokens[-1].strip(), retval=retval, label=label)
        if self.current_class is not None:
            self.current_class.add_method( self.current_function )
        else:
            self.standalone_functions.append( self.current_function )

    def _parse_param(self, line: str) -> None:
        tokens = line[2:].split(' ')
        if len(tokens) != 2:
            raise Exception(f"Wrong number of tokens when parsing a param:\n{line}")

        self.current_function.add_param(name=tokens[0].strip(), var_type=tokens[1].strip())

    def _parse_local_var(self, line: str) -> None:
        tokens = line[2:].split(' ')
        if len(tokens) != 2:
            raise Exception(f"Wrong number of tokens when parsing a local var:\n{line}")

        self.current_function.add_local_var(name=tokens[0].strip(), var_type=tokens[1].strip())

    def _parse_loop(self, line: str) -> None:
        tokens = line[2:].split(' ')
        if len(tokens) != 2:
            raise Exception(f"Wrong number of tokens when parsing a loop:\n{line}")

        self.current_function.add_loop(name=tokens[0].strip(), line_num=tokens[1].strip())

    def _parse_tags_for_function_or_class(self, line: str) -> None:
        tags = line[2:].strip()
        if self.current_function is not None:
            self.current_function.tags = tags
        else:
            if self.current_class is not None:
                self.current_class.tags = tags
            else:
                raise Exception(f"Expected a class or function to parse this line under:\n{line}")

    def parse_file(self, filename: str) -> None:
        with open(filename, "r") as inF:
            for line in inF:
                stripped_line = line.strip('\n').strip()
                if stripped_line.startswith('#'):
                    continue
                elif len(stripped_line) == 0:
                    self._finish_class()
                elif stripped_line.startswith("_ "):
                    self._check_current_class_exists(stripped_line)
                    self._parse_member_variable(stripped_line)
                    self.current_function = None
                elif stripped_line.startswith("- "):
                    self._parse_method(stripped_line)
                elif stripped_line.startswith("$ "):
                    self._check_current_function_exists(stripped_line)
                    self._parse_param(stripped_line)
                elif stripped_line.startswith("& "):
                    self._check_current_function_exists(stripped_line)
                    self._parse_local_var(stripped_line)
                elif stripped_line.startswith("( "):
                    self._check_current_function_exists(stripped_line)
                    self._parse_loop(stripped_line)
                elif stripped_line.startswith("= "):
                    self._parse_tags_for_function_or_class(stripped_line)
                else:
                    self._finish_class()
                    self._start_class(stripped_line)
        self._finish_class()