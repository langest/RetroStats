import argparse

from parse_log import parse_log

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='path to the stats file')

    args = parser.parse_args()
    tmp = parse_log(vars(args)['file'])
    print(tmp)

if __name__ == "__main__":
    main()
