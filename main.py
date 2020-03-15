# CS 4365 - Artificial Intelligence
# Assignment 3 - Knowledge Representation and Reasoning
# Nisarg Desai - npd160030
# Sanketh Reddy - spr150430


import sys


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Usage: python main.py <input file name>')
        exit(10)

    if not sys.argv[1][-3:] == '.in':
        print('Invalid file name: please pass in a ".in" filename.')

    input_file = open(sys.argv[1])
    contents = input_file.readlines()

    for line in contents:
        print(line)











