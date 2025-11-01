import argparse

parser = argparse.ArgumentParser(
    prog="basic-interpreter",
    description="An interpreter for BASIC",
)

parser.add_argument("filename")
parser.add_argument('-v', '--verbose', action='store_true')

if __name__ == "__main__": 
    args = parser.parse_args()
    # print(args.filename, args.verbose)

    with open(args.filename) as file:
        print(file.read())