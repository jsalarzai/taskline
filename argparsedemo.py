import argparse

# create parser
parser = argparse.ArgumentParser(description="A simple CLI tool")

# add arguments
parser.add_argument("name", help="jqpython", type=str)
parser.add_argument("--age", help="Your age", type=int)

# parse arguments
args = parser.parse_args()

# use arguments

print(f"Hello, {args.name}! You are {args.age} years old.")
