import typing as tp
from entities.dotFunction import DotFunction, escape_angular_brackets

class DotMemberVariable:
    def __init__(self, name: str, var_type: str=None, line_num: int=None, label: str=None):
        self.name = name
        self.line_num = line_num
        if label:
            self.label = label
        else:
            if var_type:
                self.label = f"{var_type} {name}"
            else:
                self.label = name

    def __str__(self) -> str:
        line_num_str = f"<BR/>{self.line_num}" if self.line_num \
                       else ""
        escaped_label = escape_angular_brackets(self.label)
        return " "*12 + f'<TR><TD PORT="{self.name}">{escaped_label}{line_num_str}</TD></TR>\n'

class DotClass:
    def __init__(self, name: str, filepath: str, line_num: int):
        self.class_label = name
        self.name = name.replace(':', '_')
        self.filepath = filepath
        self.line_num = line_num
        self.member_variables: tp.List[DotMemberVariable] = []
        self.methods: tp.List[DotFunction] = []

    def add_member_variable(self, name: str, *args, **kwargs) -> None:
        self.member_variables.append(DotMemberVariable(name, *args, **kwargs))

    def add_method(self, func: DotFunction) -> None:
        func.name = f"{self.name}_{func.name}"
        self.methods.append(func)

    def empty(self) -> bool:
        return len(self.member_variables) == 0 and len(self.methods) == 0

    def __str__(self) -> str:
        ans = "    subgraph cluster_" + self.name + " {\n"
        ans += f'        label="class {self.class_label}\\n{self.filepath} {self.line_num}"\n'
        if self.member_variables:
            ans += \
f"""
        {self.name}_mem_var [shape="cylinder" label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
"""
            for mem in self.member_variables:
                ans += str(mem)
            ans += "        </TABLE>>]\n"

        if self.methods:
            for f in self.methods:
                ans += str(f)

        ans += "    }\n"
        return ans
