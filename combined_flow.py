import typing as tp
import argparse

from parsers.combined import CombinedParser

from entities.dotClass import DotClass
from entities.dotFunction import DotFunction
from entities.dotLink import DotLink

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help= "Input filenames")
    parser.add_argument('--gen-inputs', action='store_true', help= \
        "Generate input file content for given filenames")
    return parser

def generate_input_files(filenames: tp.List[str]):
    for name in filenames:
        with open(name, 'w') as outF:
            outF.write(
"""# Example:
# School path/to/school.cc 15
# = bgcolor="green"
# - ctor 16 | [[B]]cons[[/B]]tructor\\n<B>
# _ name std::string
# _ students std::list<Person>
# - enrol_student 18 @ void
# $ student Person
# - is_student 20 @ bool
# $ param_name std::string
# & local_var bool
# ( while_not_exiting 24
#
# - ask_db path/to/school.cc 40
# & db_name std::string
# = fillcolor="black" color="white" fontcolor="yellow"
#
# < Person_mem_var name
# > School_is_student name | style="dashed, bold" color=red | 132

"""
            )

def parse_files(filenames: tp.List[str]) -> CombinedParser:
    comb_p = CombinedParser()

    for name in filenames:
        comb_p.parse_file(name)

    return comb_p

def write_translation_to_dot(nodes: tp.List[tp.Union[DotClass, DotFunction]], \
                             links: tp.List[DotLink]) -> str:
    ans = \
"""digraph {
    rankdir=TD
    node [shape="box" style="filled" fillcolor="white"]
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
        generate_input_files(args.filenames)
    else:
        comb_p = parse_files(args.filenames)
        print(write_translation_to_dot(comb_p.nodes, comb_p.links))