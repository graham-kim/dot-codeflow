import typing as tp
from entities.dotClass import DotClass

class NodeParser:
    def __init__(self):
        self.current_class: DotClass = None
        self.finished_classes: tp.List[DotClass] = []

    def _finish_class(self) -> None:
        if self.current_class and not self.current_class.empty():
            self.finished_classes.append(self.current_class)
        self.current_class = None

    def _check_current_class_exists(self, line: str) -> None:
        if self.current_class is None:
            raise Exception(f"Expected a class to parse this line under:\n{line}")

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

    def parse_file(self, filename: str) -> None:
        with open(filename, "r") as inF:
            for line in inF:
                stripped_line = line.strip('\n').strip()
                if len(stripped_line) == 0 or stripped_line.startswith('#'):
                    self._finish_class()
                elif stripped_line.startswith("_ "):
                    self._check_current_class_exists(stripped_line)
                    self._parse_member_variable(stripped_line)
                elif stripped_line.startswith("- "):
                    self._check_current_class_exists(stripped_line)
                    #self.current_class.add_method()
                elif stripped_line.startswith("$ "):
                    pass
                else:
                    self._finish_class()
                    self._start_class(stripped_line)
        self._finish_class()