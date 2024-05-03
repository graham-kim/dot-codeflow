import typing as tp

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


