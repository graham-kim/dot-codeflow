import typing as tp
import json

from flow import setup_parser

from parsers.grid import GridParser

with open("categories.json", 'r') as inF:
    CAT_DICT = json.load(inF)

def parse_files(filenames: tp.List[str]):
    parser = GridParser()

    for name in filenames:
        parser.parse_file(name)

    parser.print_lines(CAT_DICT)

if __name__ == '__main__':
    args = setup_parser().parse_args()
    parse_files(args.filenames)

