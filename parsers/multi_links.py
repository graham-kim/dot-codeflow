import typing as tp
from entities.dotLink import DotLink
from dataclasses import dataclass

class MultiLinkParser:
    @dataclass
    class DstWithMetadata:
        dst: str
        tags: str
        label: str
        
    def __init__(self):
        self.current_srcs: tp.List[str] = []
        self.current_dsts_data: tp.List[DstWithMetadata] = []
        self.finished_links: tp.List[DotLink] = []

    def _finish_current_links(self):
        if self.current_srcs and not self.current_dsts_data:
            raise Exception("Need to specify at least one src before finishing link")
        if not self.current_srcs and self.current_dsts_data:
            raise Exception("Need to specify at least one dst before finishing link")

        for dstdata in self.current_dsts_data:
            for src in self.current_srcs:
                if dstdata.label is not None and dstdata.label.startswith('**'):
                    link_label = dstdata.label[2:].strip()
                    link = DotLink(src, dstdata.dst, dstdata.tags, link_label)
                    for i in range(3):
                        self.finished_links.append(link)
                else:
                    link = DotLink(src, dstdata.dst, dstdata.tags, dstdata.label)
                    self.finished_links.append(link)
        self.current_dsts_data = []
        self.current_srcs = []

    def _format_link_identifier(self, tokens: tp.List[str]):
        if len(tokens) > 2:
            raise Exception("Too many spaces while specifying src or dst")
        tokens[0] = tokens[0].replace(':', '_')
        return ':'.join(tokens)

    def _add_src(self, line_num: int, line: str):
        if self.current_dsts_data:
            raise Exception(f"Finish current links before adding new sources:\n{line_num}: {line}")

        try:
            formatted_src = self._format_link_identifier( line.split(' ') )
        except Exception as ex:
            raise Exception(f"{ex}\n{line_num}: {line}")

        self.current_srcs.append(formatted_src)

    def _add_dst(self, line_num: int, line: str):
        num_sep = line.count('|')
        if num_sep > 2:
            raise Exception(f"Too many | in line while specifying dst:\n{line_num}: {line}")
        broad_tokens = line.split('|')

        try:
            formatted_dst = self._format_link_identifier( broad_tokens[0].strip().split(' ') )
        except Exception as ex:
            raise Exception(f"{ex}\n{line_num}: {line}")
        tags = None
        label = None

        if len(broad_tokens) > 1:
            label = broad_tokens[-1].strip()
        if len(broad_tokens) > 2:
            tags = broad_tokens[1].strip()

        parsed_data = self.DstWithMetadata(formatted_dst, tags, label)
        self.current_dsts_data.append(parsed_data)

    def parse_stripped_line(self, line_num: int, stripped_line: str):
        if stripped_line.startswith('#'):
            return
        elif len(stripped_line) == 0:
            self._finish_current_links()
        elif stripped_line.startswith("< "):
            self._add_src(line_num, stripped_line[2:])
        elif stripped_line.startswith("> "):
            self._add_dst(line_num, stripped_line[2:])
        elif stripped_line.startswith("<> "):
            self._add_dst(line_num, stripped_line[3:])
            self._finish_current_links()
            self._add_src(line_num, stripped_line[3:].split('|')[0].strip())
        else:
            raise Exception(f"Unexpected line to parse as link:\n{line_num}: {stripped_line}")