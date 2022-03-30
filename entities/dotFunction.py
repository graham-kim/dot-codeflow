import typing as tp

class DotParam:
    def __init__(self, name: str, var_type: str=None, label: str=None):
        self.name = name
        if label:
            self.label = label
        else:
            if var_type:
                self.label = f"{var_type} {name}"
            else:
                self.label = name

    def __str__(self) -> str:
        return " "*12 + f'<TR><TD PORT="{self.name}">{self.label}</TD></TR>\n'

class DotFunction:
    def __init__(self, name: str, line_num: int=None, retval: str=None, label: str=None):
        self.name = name
        self.line_num = line_num
        if label:
            self.label = label
        else:
            self.label = name + "()"
        self.retval = retval
        self.params: tp.List[DotParam] = []

    def add_param(self, name: str, var_type: str=None) -> None:
        label = f"{var_type} {name}" if var_type else "name"
        self.params.append( DotParam(name, label=label) )

    def __str__(self) -> str:
        line_num_str = f"<BR/>{self.line_num}" if self.line_num \
                       else ""
        ans = \
f"""
        {self.name} [shape="none" label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD PORT="call">{self.label}{line_num_str}</TD></TR>
"""
        for p in self.params:
            ans += str(p)
        if self.retval:
            ans += f'            <TR><TD PORT="retval"><B>returns</B> {self.retval}</TD></TR>'
        ans += "        </TABLE>>]\n"
        return ans