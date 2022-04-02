import typing as tp
import argparse

from parsers.node import NodeParser
from parsers.link import LinkParser

from entities.dotClass import DotClass
from entities.dotFunction import DotFunction
from entities.dotLink import DotLink

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename_prefix', help= \
        "Prefix for input filenames")
    parser.add_argument('--gen-inputs', action='store_true', help= \
        "Generate input files with the given prefix")
    return parser

node_file_suffix = "_nodes.txt"
link_file_suffix = "_links.txt"

def generate_input_files(filename_prefix: str):
    with open(filename_prefix + node_file_suffix, 'w') as outF:
        outF.write(
"""# Example:
# School path/to/school.cc 15
# - ctor 16 | [[B]]cons[[/B]]tructor\\n<B>
# _ name std::string
# _ students std::list<Person>
# - enrol_student 18 @ void
# $ student Person
# - is_student 20 @ bool
# $ name std::string
# & temp_var bool
# ( while_not_exiting 24

"""
        )

    with open(filename_prefix + link_file_suffix, 'w') as outF:
        outF.write(
"""# Example:
# Person_mem_var name
# School_is_student name
# 132.cc

"""
        )

def parse_files(filename_prefix: str) -> tp.Tuple[NodeParser, LinkParser]:
    node_p = NodeParser()
    link_p = LinkParser()

    node_p.parse_file(filename_prefix + node_file_suffix)
    link_p.parse_file(filename_prefix + link_file_suffix)

    return node_p, link_p

def write_translation_to_dot(nodes: tp.List[tp.Union[DotClass, DotFunction]], \
                             links: tp.List[DotLink]) -> str:
    ans = \
"""digraph {
    rankdir=TD
    node [shape="box"]
"""
    for node in nodes:
        ans += f"\n{node}"
    ans += "\n"
    for link in links:
        ans += str(link)
    ans += "}"
    return ans

if __name__ == '__main__':
    args = setup_parser().parse_args()
    if args.gen_inputs:
        generate_input_files(args.filename_prefix)
    else:
        node_p, link_p = parse_files(args.filename_prefix)
        nodes = node_p.finished_classes + node_p.standalone_functions
        print(write_translation_to_dot(nodes, link_p.finished_links))