import typing as tp
import json

from flow import setup_parser

from parsers.shorthand import ShorthandParser

with open("categories.json", 'r') as inF:
    CAT_DICT = json.load(inF)

def parse_files(filenames: tp.List[str]):
    parser = ShorthandParser()

    for name in filenames:
        parser.parse_file(name)

    parser.print_lines(CAT_DICT)

if __name__ == '__main__':
    args = setup_parser().parse_args()
    parse_files(args.filenames)

