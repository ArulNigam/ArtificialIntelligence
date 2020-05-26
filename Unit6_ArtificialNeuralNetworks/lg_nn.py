# Name: Arul Nigam
# Period 3
import copy
import sys, os, math, random

# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
import time


def transfer(t_funct, input):
    if t_funct == "T1":  # linear function
        return input
    elif t_funct == "T2":  # ramp function
        return [max(0, x) for x in input]
    elif t_funct == "T3":  # logistic
        return [1 / (1 + math.exp(-x)) for x in input]
    else:  # t_funct == "T4" # sigmoid
        return [-1 + 2 / (1 + math.exp(-x)) for x in input]


def deriv_transfer(t_funct, input):
    if t_funct == "T1":  # linear function
        return 1
    elif t_funct == "T2":  # ramp function
        return 0 if input < 0 else 1
    elif t_funct == "T3":  # logistic
        return (1 / (1 + math.exp(-input))) * (1 - (1 / (1 + math.exp(-input))))
    else:  # t_funct == "T4" # sigmoid
        return 2 * (1 / (1 + math.exp(-input))) * (1 - (1 / (1 + math.exp(-input))))


# example: 4 inputs, 12 weights, and 3 stages(the number of next layer nodes)
# weights are listed like Example Set 1 #4 or on the NN_Lab1_description note
# returns a list of dot_product result. the len of the list == stage
# Challenge? one line solution is possible
def dot_product(input, weights, stage):  # activation, weights_list[i], i
    num_neurons = len(weights) // len(input)
    output = list()
    for n in range(num_neurons):
        output.append(sum([weights[n * len(input) + i] * input[i] for i in range(len(input))]))
    return output


# file has weights information. Read file and store weights in a list or a nested list
# input_vals is a list which includes input values from terminal
# t_funct is a string, e.g. 'T1'
# forward_pass the whole network (complete the whole forward feeding)
# and return a list of output(s)
def forward_pass(weights_list, input_vals, t_funct):
    num_layers = len(weights_list)
    activation = input_vals
    activations = [activation]
    for i in range(num_layers - 1):
        dot_prod = dot_product(activation, weights_list[i], i)
        activation = transfer(t_funct, dot_prod)
        activations.append(activation)
    final_activation = sum([activation[i] * weights_list[-1][i] for i in range(len(activation))])
    return final_activation, activations


def loss(actual, prediction):
    return math.pow((actual - prediction), 2)


def deriv(actual, prediction, weights, t_funct, input):
    reversed_weights = weights[::-1]
    reversed_inputs = input[::-1]
    derivatives = []
    for i, layer in enumerate(reversed_weights):
        layer_derivatives = []
        for j, weight in enumerate(layer):
            if i == 0:
                derivative = (prediction - actual) * reversed_inputs[i][j]
            elif i == 1:
                z = dot_product(reversed_inputs[i], reversed_weights[i], 0)[0]
                derivative = (prediction - actual) * reversed_weights[i - 1][0] * deriv_transfer(t_funct, z) * \
                             reversed_inputs[i][j]
            else:
                if j < len(layer) // 2:
                    delta_index = 0
                else:
                    delta_index = 1
                z1 = dot_product(reversed_inputs[i], reversed_weights[i], 0)[0]
                z2 = dot_product(reversed_inputs[i - 1], reversed_weights[i - 1], 0)[0]
                derivative = (prediction - actual) * reversed_weights[i - 2][0] * deriv_transfer(t_funct, z2) * \
                             reversed_weights[i - 1][delta_index] * deriv_transfer(t_funct, z1) * reversed_inputs[i][
                                 j % len(reversed_inputs[-1])]
            layer_derivatives.append(derivative)
        derivatives.append(layer_derivatives)
    return derivatives[::-1]


def back_propagate(weights, actuals, predictions, t_funct, inputs):
    multiple = 0.1  # learning rate
    count = 0
    for actual, prediction, input in zip(actuals, predictions, inputs):
        if count == 0:
            derivatives = deriv(actual, prediction, weights, t_funct, input)
        else:
            derivatives_datapoint = deriv(actual, prediction, weights, t_funct, input)
            derivatives = [[derivatives[i][j] + derivatives_datapoint[i][j] for j in range(len(derivatives[i]))] for i
                           in range(len(derivatives))]
        count += 1
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weights[i][j] = weights[i][j] - (multiple * derivatives[i][j])  # gradient descent
    return weights


def main():
    initial_time = time.perf_counter()
    args = sys.argv[1:]
    file, inputs, t_funct, transfer_found = '', [], 'T3', False
    for arg in args:
        if os.path.isfile(arg):
            file = arg
        elif not transfer_found:
            t_funct, transfer_found = arg, True
        else:
            inputs.append(float(arg))
    if len(file) == 0: exit("Error: Logic file is not given")
    f = open(file, 'r')
    inp = f.readlines()
    inputs = []
    outputs = []
    for line in inp:
        temp = line.split("=>")
        inputs.append([int(feature) for feature in temp[0].strip().split(" ")])
        outputs.append(int(temp[1].strip()))
    weights = [[random.randrange(-200, 200) / 100 for i in range(2 * (1 + len(inputs[0])))],
               [random.randrange(-200, 200) / 100 for i in range(2)], [random.randrange(-200, 200) / 100]]
    temp_inputs = copy.deepcopy(inputs)
    inps = list()
    for temp_inp in temp_inputs:
        inp = temp_inp
        inp.append(1)
        inps.append(inp)
    epoch = 0
    error_sum = 0
    while epoch < 40000:
        if error_sum > 1:
            weights = [[random.randrange(-200, 200) / 100 for i in range(2 * (1 + len(inputs[0])))],
                       [random.randrange(-200, 200) / 100 for i in range(2)], [random.randrange(-200, 200) / 100]]
        lis, activations, errors = [], [], []
        for t in range(len(inps)):
            li, activation = forward_pass(weights, inps[t], t_funct)
            lis.append(li)
            activations.append(activation)
            errors.append(math.pow(li - outputs[t], 2))
        weights = back_propagate(weights, outputs, lis, t_funct, activations)
        error_sum = sum(errors)
        epoch += 1
        if error_sum <= 0.01:
            epoch = math.inf
    print("Layer counts ", [1 + len(inputs[0]), 2, 1, 1])
    print("Errors: ", errors)
    print("Weights: ")
    for w in weights:
        print(w)
    print("Time: ", time.perf_counter() - initial_time)
    return weights

if __name__ == '__main__': main()
