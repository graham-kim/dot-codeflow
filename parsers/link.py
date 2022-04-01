import typing as tp
from entities.dotLink import DotLink

class LinkParser:
    def __init__(self):
        self._reset_link()
        self.finished_links: tp.List[DotLink] = []

    def _reset_link(self):
        self.src: str = None
        self.dst: str = None
        self.tags: str = None
        self.label: str = None

    def _finish_link(self, line_num: tp.Union[int, str]):
        if self.src is not None:
            if self.dst is None:
                raise Exception(f"Incomplete link detected at {line_num}")
            self.finished_links.append( DotLink(self.src, self.dst, tags=self.tags, label=self.label) )
            self._reset_link()

    def _parse_tags_and_label(self, line: str) -> None:
        if not '|' in line:
            self.label = line
        else:
            tokens = line.split('|')
            label = tokens[1].strip()
            self.label = label if len(label) > 0 else None
            self.tags = tokens[0].strip()

    def parse_file(self, filename: str) -> None:
        def parse_src_or_dst(line):
            tokens = line.split(' ')
            if len(tokens) > 2:
                raise Exception(f"Too many spaces in line while specifying src or dst:\n{line}")
            tokens[0] = tokens[0].replace(':', '_')
            return ':'.join(tokens)

        with open(filename, "r") as inF:
            for i, line in enumerate(inF):
                stripped_line = line.strip('\n').strip()
                if stripped_line.startswith('#'):
                    continue
                elif len(stripped_line) == 0:
                    self._finish_link(i)
                else:
                    if self.src is None:
                        self.src = parse_src_or_dst(stripped_line)
                    elif self.dst is None:
                        self.dst = parse_src_or_dst(stripped_line)
                    elif self.label is None:
                        self._parse_tags_and_label(stripped_line)
                    else:
                        raise Exception(f"A line too many (line_num: {i}) when specifying a link:\n{stripped_line}")
        self._finish_link("EOF")