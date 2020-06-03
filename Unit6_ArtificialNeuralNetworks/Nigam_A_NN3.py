# Name: Arul Nigam
# Period 3
import copy
import sys, os, math, random, time


# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
import time, re


def create_data(inp):
    # inp = inp.strip()
    training_inputs = []
    training_outputs = []
    '''if "=" in inp:
        r = inp[9:]
    else:
        r = inp[8:]'''
    for i in range(20480): # training data
        inp_copy = copy.deepcopy(inp)
        x = random.uniform(-1.50, 1.50)
        y = random.uniform(-1.50, 1.50)
        inp_copy = re.sub("x", str(x), inp_copy)
        inp_copy = re.sub("y", str(y), inp_copy)
        training_inputs.append([x, y, 1])
        training_outputs.append(int(eval(inp_copy)))
    return training_inputs, training_outputs


def transfer(t_funct, input):
    return [1 / (1 + math.e ** (-x)) for x in input] # ** instead of exp to handle bigger nums
    '''if t_funct == "T1":  # linear function
        return input
    elif t_funct == "T2":  # ramp function
        return [max(0, x) for x in input]
    elif t_funct == "T3":  # logistic
        return [1 / (1 + math.exp(-x)) for x in input]
    else:  # t_funct == "T4" # sigmoid
        return [-1 + 2 / (1 + math.exp(-x)) for x in input]'''


def deriv_transfer2(t_funct, inputs):
    return [(1 / (1 + math.e ** (-input))) * (1 - (1 / (1 + math.e ** (-input)))) for input in inputs]

def deriv_transfer(t_funct, input):
    return (1 / (1 + math.e ** (-input))) * (1 - (1 / (1 + math.e ** (-input))))
    '''if t_funct == "T1":  # linear function
        return 1
    elif t_funct == "T2":  # ramp function
        return 0 if input < 0 else 1
    elif t_funct == "T3":  # logistic
        return (1 / (1 + math.exp(-input))) * (1 - (1 / (1 + math.exp(-input))))
    else:  # t_funct == "T4" # sigmoid
        return 2 * (1 / (1 + math.exp(-input))) * (1 - (1 / (1 + math.exp(-input))))'''


# example: 4 inputs, 12 weights, and 3 stages(the number of next layer nodes)
# weights are listed like Example Set 1 #4 or on the NN_Lab1_description note
# returns a list of dot_product result. the len of the list == stage
# Challenge? one line solution is possible
def dot_product(input, weights, stage=0):  # activation, weights_list[i], i
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

def deriv2(actual, prediction, weights, t_funct, input):
    reversed_weights = weights[::-1]
    reversed_inputs = input[::-1]
    derivatives = []
    # delta = []
    for i, layer in enumerate(reversed_weights):
        if i == 0:
            delta = [prediction - actual]
            print(prediction - actual)
        else: # not last layer
            error = dot_product(reversed_weights[i - 1], delta)
            df_dz = deriv_transfer(t_funct, reversed_inputs[i])
            print("e", error)
            print("d", df_dz)
            print("delta", delta)
            delta = [error[0] * drv for drv in df_dz]
        derivative = [delta[j] * reversed_inputs[i][j] for j in range(len(reversed_inputs[i]))]
        print("drv", len(derivative))
        print("rev weights", len(reversed_weights[i]))
        derivatives.append(derivative)
    return derivatives[::-1]


def deriv(actual, prediction, weights, t_funct, input):
    reversed_weights = weights[::-1]
    reversed_inputs = input[::-1]
    derivatives = []
    for i, layer in enumerate(reversed_weights):
        layer_derivatives = []
        for j, weight in enumerate(layer):
            if i == 0:
                derivative = (prediction - actual) * reversed_inputs[i][j % len(reversed_inputs[i])]
            elif i == 1:
                z1 = dot_product(reversed_inputs[i], reversed_weights[i], 0)[0]
                # z2 = dot_product(reversed_weights[i - 1], reversed_inputs[i - 1], 0)[0]
                # print(j, reversed_weights[i - 1])
                derivative = (prediction - actual) * reversed_weights[i - 1][0] * deriv_transfer(t_funct, z1) * \
                             reversed_inputs[i][j % len(reversed_inputs[i])]
            else:
                if j < len(layer) // 2:
                    delta_index = 0
                else:
                    delta_index = 1
                z1 = dot_product(reversed_inputs[i], reversed_weights[i], 0)[0]
                z2 = dot_product(reversed_inputs[i - 1], reversed_weights[i - 1], 0)[0]
                # z3 = dot_product(reversed_inputs[i - 2], reversed_weights[i - 2], 0)[0]
                derivative = (prediction - actual) * reversed_inputs[i - 2][0] * deriv_transfer(t_funct, z2) * \
                             reversed_weights[i - 1][delta_index] * deriv_transfer(t_funct, z1) * reversed_inputs[i][
                                 j % len(reversed_inputs[-1])]
            layer_derivatives.append(derivative)
        derivatives.append(layer_derivatives)
    return derivatives[::-1]


def back_propagate(weights, actuals, predictions, t_funct, inputs):
    multiple = 0.25  # learning rate
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
            # print("derivs", i, j, derivatives[i])
            weights[i][j] = weights[i][j] - (multiple * derivatives[i][j])  # gradient descent
    return weights


def main():
    start_time = time.time()
    input_equation = sys.argv[1]
    inputs, outputs = create_data(input_equation)
    # r = float(str(r))
    t_funct = 'T3'
    node_count = [10, 1] # number of nodes in hidden layer
    weights = []
    starting_error = math.inf
    while time.time() - start_time < 80:
        error_sum = 0
        temp_weights = [[random.uniform(-2.0, 2.0) for i in range(3 * node_count[0])],
                   [random.uniform(-2.0, 2.0) for i in range(node_count[0] * node_count[1])],
                   [random.uniform(-2.0, 2.0) for i in range(node_count[1])]]
        step = 0
        batch_size = 32
        lis, activations = [], []
        full_loop = True
        for input, output in zip(inputs, outputs):
            li, activation = forward_pass(temp_weights, input, t_funct)
            lis.append(li)
            activations.append(activation)
            step += 1
            error_sum += math.pow(li - output, 2)
            if error_sum >= starting_error:
                full_loop = False
                break
            if step % batch_size == 0 and step >= batch_size:
                temp_weights = back_propagate(temp_weights, outputs[step - batch_size: step], lis, t_funct, activations)
                lis, activations = [], []
        if full_loop and error_sum < starting_error:
            starting_error = error_sum
            weights = copy.deepcopy(temp_weights)
    epoch = 0
    while epoch < 1:
        lis, activations = [], []
        step = 0
        batch_size = 32
        for input, output in zip(inputs, outputs):
            li, activation = forward_pass(weights, input, t_funct)
            lis.append(li)
            activations.append(activation)
            step += 1
            if step % batch_size == 0 and step >= batch_size:
                weights = back_propagate(weights, outputs[step - batch_size: step], lis, t_funct, activations)
                if time.time() - start_time > 99.5:
                    print("Layer counts ", [3, node_count[0], node_count[1], 1])
                    for w in weights:
                        print(w)
                lis, activations = [], []
        epoch += 1
    print("Layer counts ", [3, node_count[0], node_count[1], 1])
    for w in weights:
        print(w)
    print("***********************DONE***********************", time.time() - start_time)
    return weights


if __name__ == '__main__': main()
