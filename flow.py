import argparse

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename_prefix', help= \
        "Prefix for input filenames")
    parser.add_argument('--gen_inputs', action='store_true', help= \
        "Generate input files with the given prefix")
    return parser

node_file_suffix = "_nodes.txt"
link_file_suffix = "_links.txt"

def generate_input_files(filename_prefix: str):
    with open(filename_prefix + node_file_suffix, 'w') as outF:
        outF.write(
"""
# comment 1
# comment 2
"""
        )

    with open(filename_prefix + link_file_suffix, 'w') as outF:
        outF.write(
"""
# comment 1
# comment 2
"""
        )

def print_translation_to_dot(filename_prefix: str):
    print("digraph {")
    print('    rankdir=TD')
    print('    node [shape="box"]')
    print("}")

if __name__ == '__main__':
    args = setup_parser().parse_args()
    if args.gen_inputs:
        generate_input_files(args.filename_prefix)
    else:
        print_translation_to_dot(args.filename_prefix)