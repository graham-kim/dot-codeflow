import typing as tp

def escape_angular_brackets(label: str) -> str:
    return label.replace('<', '&lt;').replace('>', '&gt;')

def substitute_angular_brackets_after_escaping(label: str) -> str:
    return escape_angular_brackets(label)\
            .replace('[[', '<').replace(']]', '>').replace('\\n', '<BR/>')

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
        escaped_label = substitute_angular_brackets_after_escaping(self.label)
        return " "*12 + f'<TR><TD PORT="{self.name}">{escaped_label}</TD></TR>\n'

class DotLocalVar(DotParam):
    def __str__(self) -> str:
        escaped_label = substitute_angular_brackets_after_escaping(self.label)
        return " "*12 + f'<TR><TD PORT="{self.name}"><B>local</B> {escaped_label}</TD></TR>\n'

class DotLoop(DotParam):
    def __str__(self) -> str:
        escaped_label = substitute_angular_brackets_after_escaping(self.label)
        return " "*12 + f'<TR><TD PORT="{self.name}"><U>loop</U> {escaped_label}</TD></TR>\n'

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
        self.localvars: tp.List[DotLocalVar] = []
        self.loops: tp.List[DotLoop] = []

    def add_param(self, name: str, var_type: str=None) -> None:
        label = f"{var_type} {name}" if var_type else "name"
        self.params.append( DotParam(name, label=label) )

    def add_local_var(self, name: str, var_type: str=None) -> None:
        label = f"{var_type} {name}" if var_type else "name"
        self.localvars.append( DotLocalVar(name, label=label) )

    def add_loop(self, name: str, line_num: str=None) -> None:
        label = name
        if line_num:
            label += f" {line_num}"
        self.loops.append( DotLoop(name, label=label) )

    def __str__(self) -> str:
        line_num_str = f"<BR/>{self.line_num}" if self.line_num \
                       else ""
        escaped_label = substitute_angular_brackets_after_escaping(self.label)
        ans = \
f"""
        {self.name} [shape="none" label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD PORT="call">{escaped_label}{line_num_str}</TD></TR>
"""
        for p in self.params:
            ans += str(p)
        for v in self.localvars:
            ans += str(v)
        for l in self.loops:
            ans += str(l)
        if self.retval:
            escaped_retval = substitute_angular_brackets_after_escaping(self.retval)
            ans += f'            <TR><TD PORT="retval"><B>returns</B> {escaped_retval}</TD></TR>\n'
        ans += "        </TABLE>>]\n"
        return ans