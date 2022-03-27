import typing as tp

class DotMemberVariable:
    def __init__(self, name: str, line_num: int=None, var_type: str=None, label: str=None):
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
        return " "*12 + f'<TR><TD PORT="{self.name}">{self.label}{line_num_str}</TD></TR>\n'

class DotClass:
    def __init__(self, name: str, filepath: str, line_num: int):
        self.name = name
        self.filepath = filepath
        self.line_num = line_num
        self.member_variables: tp.List[DotMemberVariable] = []

    def add_member_variable(self, name: str, *args, **kwargs):
        self.member_variables.append(DotMemberVariable(f"{self.name}_{name}", *args, **kwargs))

    def __str__(self) -> str:
        ans = "    subgraph cluster_" + self.name + " {\n"
        ans += f'        label="class {self.name}\\n{self.filepath} {self.line_num}"\n'
        if self.member_variables:
            ans += \
f"""
        {self.name}_mem_var [shape="cylinder" label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
"""
            for mem in self.member_variables:
                ans += str(mem)
            ans += "        </TABLE>>]\n"

        ans += "    }\n"
        return ans
