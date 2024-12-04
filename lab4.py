#lab4.py

# Starter code for lab 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chris Cyr
# cyrc@uci.edu
# 12436037

import random

"""
The default numbers here are generally good enough to create a rich tree. 
You are free to play with the numbers if you want. Lower numbers will simplify the results, 
larger numbers will take more time to render and create hundreds of acorns.
"""

TREE_DEPTH = 5
NODE_DEPTH = 5

def tree_builder(nodes:list, level:int, acorn:str) -> list:
    """
    Builds a tree using the random integers selected from the tree_depth and node_depth defaults
    """
    r = random.randrange(1, NODE_DEPTH)
    for i in range(r):
        if level < TREE_DEPTH:
            level_id  = f"L{level}-{i}"
            if level_id == acorn:
                level_id += "(acorn)"
            n = [level_id]
            nodes.append(tree_builder(n, level+1, acorn_placer()))

    return nodes


acorn_count = 0
output = []
branch = []


def hatred(tree):
    global acorn_count
    global output
    global branch
    for i in tree:
        if type(i) == list:
            hatred(i)
        elif type(i) == str:
            if i[5:10] == "acorn" and (int(i[1]) > int(branch[-1][1]) or int(i[3]) > int(branch[-1][3])):
                acorn_count += 1
                branch.append(i[0:4])
                output.append(branch)
                branch = []
            elif len(branch) > 0 and int(i[3]) < int(branch[-1][3]):
                branch = [i]
            else:
                branch.append(i)


def tester(tree):
    """Just for testing the call statement is commented out"""
    for i in tree:
        if type(i) == list:
            tester(i)
        elif type(i) == str:
            if i[5:10] == "acorn":
                print(i)
            else:
                print(i + " -> ", end='')


def acorn_placer() -> str:
    """
    Returns a random acorn location based on tree_depth and node_depth defaults
    """
    return f"L{random.randrange(1,TREE_DEPTH)}-{random.randrange(1,NODE_DEPTH)}"

def run():
    # create a tree and start placing acorns
    tree = tree_builder([], 1, acorn_placer())
    # print the tree for testing. 
    
    # insert your solution code here
    global output
    global acorn_count

    #tester(tree)
    hatred(tree)
    print(f"You have {acorn_count} acorns on your tree!")
    print("They are located on the following branches:\n")
    for i in range(len(output)):
        for j in range(len(output[i]) - 1):
            print(output[i][j] + " -> ", end='')
        print(output[i][len(output[i]) - 1])
    # end solution

if __name__ == "__main__":
    print("Welcome to PyAcornFinder! \n")

    run()
