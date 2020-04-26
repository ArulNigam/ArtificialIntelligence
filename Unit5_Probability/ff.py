# Name: Arul Nigam
# Period 3

import sys, os, math


# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
def transfer(t_funct, input):
    return []


# example: 4 inputs, 12 weights, and 3 stages(the number of next layer nodes)
# weights are listed like Example Set 1 #4 or on the NN_Lab1_description note
# returns a list of dot_product result. the len of the list == stage
# Challenge? one line solution is possible
def dot_product(input, weights, stage):
    return []


# file has weights information. Read file and store weights in a list or a nested list
# input_vals is a list which includes input values from terminal
# t_funct is a string, e.g. 'T1'
# evaluate the whole network (complete the whole forward feeding)
# and return a list of output(s)
def evaluate(file, input_vals, t_funct):
    return []


def main():
    args = sys.argv[1:]
    file, inputs, t_funct, transfer_found = '', [], 'T1', False
    for arg in args:
        if os.path.isfile(arg):
            file = arg
        elif not transfer_found:
            t_funct, transfer_found = arg, True
        else:
            inputs.append(float(arg))
    if len(file) == 0: exit("Error: Weights file is not given")
    li = (evaluate(file, inputs, t_funct))
    for x in li:
        print(x, end=' ')


if __name__ == '__main__': main()