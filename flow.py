import typing as tp
import argparse

from parsers.general import GeneralParser
from printers.pretty import pretty_print_with_global_attr

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help= "Input filenames")
    parser.add_argument('--gen-inputs', action='store_true', help= \
        "Generate input file content for given filenames")
    parser.add_argument('--rankdir', default="TD", help="Direction to draw graph")
    return parser

def generate_input_files(filenames: tp.List[str]):
    for name in filenames:
        with open(name, 'w') as outF:
            outF.write(
"""# Example:
/@ Clus1

- A
- B
= fillcolor="red"

< A
> B | @3*@

@ A B

/@ SubAlpha | the [[B]]bold[[/B]] @this@
= bgcolor=yellow
- C | node C
@/

< A
< B
= color=red,style="bold, dashed"
<> SubAlpha_C | link is [[font color="red"]]here[[/font]]
> SubAlpha

@/

""")

def parse_files(filenames: tp.List[str]):
    parser = GeneralParser()

    for name in filenames:
        parser.parse_file(name)

    return parser.get_pydot_dot()

if __name__ == '__main__':
    args = setup_parser().parse_args()
    if args.gen_inputs:
        generate_input_files(args.filenames)
    else:
        dot, ranksame_lists = parse_files(args.filenames)
        pretty_print_with_global_attr(dot, args, ranksame_lists)
