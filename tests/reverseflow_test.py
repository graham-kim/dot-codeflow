import unittest
import subprocess
import os

class ReverseFlowTest(unittest.TestCase):
    def test_reverse_and_forward(self):
        # Example input content
        example_input = '''# Example:
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

@/'''
        input_path = 'tests/example_input.txt'
        reverse_input_path = 'tests/reverse_input.txt'

        # Write example input file
        with open(input_path, 'w') as f:
            f.write(example_input)

        # Run flow.py to generate temp.dot
        subprocess.run(['python', 'flow.py', input_path], check=True)
        dot1_path = 'temp.dot'
        with open(dot1_path, 'r') as f:
            dot1_content = f.read()

        # Run reverseflow.py on temp.dot
        subprocess.run(['python', 'reverseflow.py', dot1_path, reverse_input_path], check=True)

        # Run flow.py on reverse_input.txt to generate temp.dot again
        subprocess.run(['python', 'flow.py', reverse_input_path], check=True)
        with open(dot1_path, 'r') as f:
            dot2_content = f.read()

        # Compare the two dot files
        self.assertEqual(dot1_content, dot2_content)

        # Clean up
        os.remove(input_path)
        os.remove(reverse_input_path)
        os.remove(dot1_path)

if __name__ == '__main__':
    unittest.main()
