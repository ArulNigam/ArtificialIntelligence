# Name: Arul Nigam
# Period 3

import sys, os, math


# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
def transfer(t_funct, input):
    if t_funct == "T1": # linear function
        return input
    elif t_funct == "T2": # ramp function
        return [max(0, x) for x in input]
    elif t_funct == "T3": # logistic
        return [1/(1 + math.exp(-x)) for x in input]
    else: # t_funct == "T4" # sigmoid
        return [-1 + 2/(1 + math.exp(-x)) for x in input]


# example: 4 inputs, 12 weights, and 3 stages(the number of next layer nodes)
# weights are listed like Example Set 1 #4 or on the NN_Lab1_description note
# returns a list of dot_product result. the len of the list == stage
# Challenge? one line solution is possible
def dot_product(input, weights, stage):
    num_neurons = len(weights) // len(input)
    output = list()
    for n in range(num_neurons):
        output.append(sum([weights[n * len(input) + i] * input[i] for i in range(len(input))]))
    return output


# file has weights information. Read file and store weights in a list or a nested list
# input_vals is a list which includes input values from terminal
# t_funct is a string, e.g. 'T1'
# evaluate the whole network (complete the whole forward feeding)
# and return a list of output(s)
def evaluate(file, input_vals, t_funct):
    weights_file = open(file, 'r')
    weights_list = list()
    for line in weights_file:
        weights_list.append([float(i) for i in line.split(" ")])
    num_layers = len(weights_list)
    activation = input_vals
    for i in range(num_layers - 1):
        dot_prod = dot_product(activation, weights_list[i], i)
        activation = transfer(t_funct, dot_prod)
    final_activation = [activation[i] * weights_list[-1][i] for i in range(len(activation))]
    return final_activation


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
    ret = ""
    for x in li:
        ret += str(x)
        ret += ' '
    print(ret[:-1])
    return ret[:-1]


if __name__ == '__main__': main()
