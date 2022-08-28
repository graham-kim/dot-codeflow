import typing as tp
import argparse

from parsers.general import GeneralParser

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
""")

def parse_files(filenames: tp.List[str]):
    parser = GeneralParser()

    for name in filenames:
        parser.parse_file(name)

    return parser.get_pydot_dot()

def pretty_print_dot(dot):
    dot.write("temp.dot")

    indent_level = 0
    with open("temp.dot", "r") as inF:
        for line in inF:
            if line.strip().endswith("}"):
                indent_level -= 1

            print(" "*indent_level*4 + line)

            if line.strip().endswith("{"):
                indent_level += 1

if __name__ == '__main__':
    args = setup_parser().parse_args()
    if args.gen_inputs:
        generate_input_files(args.filenames)
    else:
        dot = parse_files(args.filenames)
        pretty_print_dot(dot)
