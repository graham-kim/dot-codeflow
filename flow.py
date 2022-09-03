import typing as tp
import argparse

from parsers.general import GeneralParser

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

def pretty_print_with_global_attr(dot, args, ranksame_lists: tp.List[tp.List[str]]):
    dot.write("temp.dot")

    indent_level = 0
    with open("temp.dot", "r") as inF:
        for i,line in enumerate(inF):
            if line.strip().endswith("}"):
                indent_level -= 1
                if indent_level == 0: # about to print the last '}' in the file
                    for list in ranksame_lists:
                        print('    {rank=same;' + ";".join(list) + '}')

            if line.strip().startswith("subgraph"):
                print("")


            print(" "*indent_level*4 + line.strip('\n').strip('\r'))

            if i == 0:
                print(f'    rankdir={args.rankdir}')
                print('    node [shape="box" style="filled" fillcolor="white"]')
                if ranksame_lists:
                    print('    newrank=true')

            if line.strip().endswith("{"):
                indent_level += 1

if __name__ == '__main__':
    args = setup_parser().parse_args()
    if args.gen_inputs:
        generate_input_files(args.filenames)
    else:
        dot, ranksame_lists = parse_files(args.filenames)
        pretty_print_with_global_attr(dot, args, ranksame_lists)
