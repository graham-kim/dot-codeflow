import typing as tp
import json

from flow import setup_parser

from parsers.shorthand import ShorthandParser

CAT_DICT = {
    "x": 'fillcolor="#FF9999"',
    "o": 'fillcolor="#55FF55"',
    ".": 'shape=oval'
}

with open('categories.json', 'w') as outF:
    json.dump(CAT_DICT, outF, indent=4)

def parse_files(filenames: tp.List[str]):
    parser = ShorthandParser()

    for name in filenames:
        parser.parse_file(name)

    parser.print_lines(CAT_DICT)

if __name__ == '__main__':
    args = setup_parser().parse_args()
    parse_files(args.filenames)

