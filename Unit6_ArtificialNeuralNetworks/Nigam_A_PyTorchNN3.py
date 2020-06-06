# Name: Arul Nigam
# Period 3
import copy
import math
import random
import re
import sys
import torch


class SquareNet(torch.nn.Module):
    def __init__(self):
        super(SquareNet, self).__init__()  # superclass is torch.nn.Module
        self.fc1 = torch.nn.Linear(1, 2, bias=True)  # fc1 => fully-connected layer 1; Linear => layer object
        self.fc2 = torch.nn.Linear(2, 2, bias=False)  # cascading layers
        self.fc3 = torch.nn.Linear(2, 1, bias=False)  # cascading layers
        # super(SquareNet, self).__init__()  # superclass is torch.nn.Module

    def forward(self, x):
        # print(x, type(x))
        # temp1, temp2 = self.fc1(x)
        # print(temp1, temp2)
        x = torch.nn.functional.sigmoid(self.fc1(x))  # outputs tensor of layer 1
        x = torch.nn.functional.sigmoid(self.fc2(x))  # outputs tensor of layer 2
        x = 2.25 * torch.nn.functional.sigmoid(self.fc3(x))  # outputs tensor of layer 3 # scaled sigmoid
        return x

    def reset_parameters(self):
        for m in self.modules():
            if isinstance(m, torch.nn.Linear):
                torch.nn.init.kaiming_normal_(m.weight)


class SquareDataset(torch.utils.data.Dataset):
    def __init__(self, inputs, outputs):
        self.data = inputs
        self.labels = outputs

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return torch.tensor([self.data[index]]), torch.tensor([self.labels[index]])


class SquareTestingDataset(torch.utils.data.Dataset):
    def __init__(self, inputs, outputs):
        self.data = inputs
        self.labels = outputs

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return torch.tensor([self.data[index][0]]), torch.tensor([self.data[index][1]]), torch.tensor(
            [self.labels[index]])


def create_testing_data(inp):
    # inp = inp.strip()
    training_inputs = []
    training_outputs = []
    for i in range(100000):  # training data
        inp_copy = copy.deepcopy(inp)
        # print(inp_copy)
        x = random.uniform(-1.50, 1.50)
        y = random.uniform(-1.50, 1.50)
        inp_copy = re.sub("x", str(x), inp_copy)
        inp_copy = re.sub("y", str(y), inp_copy)
        training_inputs.append([x, y, 1])
        training_outputs.append(int(eval(inp_copy)))
        # print(training_inputs[i], training_outputs[i])
    print(training_inputs)
    print(training_outputs)
    return training_inputs, training_outputs


def square_create_data(n):
    training_inputs = []
    training_outputs = []
    inputs = [-1.50 + 3 / n * i for i in range(n)]
    random.shuffle(inputs)
    for x in inputs:  # training data
        training_inputs.append(x)
        training_outputs.append(x ** 2)
    return training_inputs, training_outputs


def main():
    input_equation = sys.argv[1]
    num = input_equation[input_equation.find(".") - 1:]
    num = num[:len(num) - 1]
    c = torch.tensor(float(num))
    symbol = ""
    ind = input_equation.find("<")
    if ind > -1:  # contains
        symbol = "<"
        if input_equation[ind + 1] == "=":
            symbol = "<="
    ind2 = input_equation.find(">")
    if ind2 > -1:  # contains
        symbol = ">"
        if input_equation[ind2 + 1] == "=":
            symbol = ">="
    inputs, outputs = square_create_data(5000000)  # amount of TRAINING DATA
    dataset = SquareDataset(inputs, outputs)
    net = SquareNet()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.1)  # Specifies the optimization
    criterion = torch.nn.MSELoss()  # Specifies the loss function
    epochs = 5
    net = net.train()
    for e in range(epochs):
        count = 0
        running_loss = 0
        for i in range(len(inputs)):
            x, label = dataset[i]
            predicted = net(x)
            optimizer.zero_grad()  # Zeros the gradient
            # forward + backward + optimize
            loss = criterion(predicted, label)  # Calculate loss for sample
            loss.backward()  # Backpropgation step
            optimizer.step()  # Updates weights using computed gradients
            new_loss = loss.item()
            running_loss += new_loss
            if count % 10000 == 9999:  # print every 500 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (e + 1, count + 1, running_loss / (count + 1)))
                # running_loss = 0.0
            count += 1  # Increment the counter
        if running_loss / count > 0.01 and e != epochs - 1:
        # if new_loss > 0.005 and e != epochs - 1:
            net.reset_parameters()
            print("RESET")
    net = net.eval()  # FINAL MODEL
    testing_inputs, testing_outputs = create_testing_data(input_equation)
    testing_dataset = SquareTestingDataset(testing_inputs, testing_outputs)
    symbol_to_sign = {">": 0, ">=": 0, "<": 1, "<=": 1}
    count = 0
    count_correct = 0
    for x, y, label in testing_dataset:
        predicted_x = net(x)
        predicted_y = net(y)
        predicted = round(abs(
            symbol_to_sign[symbol] - torch.nn.functional.sigmoid(predicted_x + predicted_y - c).detach().numpy()[0]))
        if predicted == label:
            count_correct += 1
        count += 1  # Increment the counter
    print("total % correct = ", count_correct / count)

    weights = list()
    weights_layer = [[k, v] for k, v in net.state_dict().items()]
    # r = 1 / (1 + math.e ** (-c.numpy()))
    r_const = 1 + 1 / math.e  # recip of inv of sigmoid at x = 1 (bias)
    weights_3_5 = [weights_layer[0][1].numpy()[0][0], 0, weights_layer[1][1].numpy()[0],
                   weights_layer[0][1].numpy()[1][0], 0, weights_layer[1][1].numpy()[1], 0,
                   weights_layer[0][1].numpy()[0][0], weights_layer[1][1].numpy()[0], 0,
                   weights_layer[0][1].numpy()[1][0], weights_layer[1][1].numpy()[1], 0, 0, 1]
    weights.append(weights_3_5)
    weights_5_5 = [weights_layer[2][1].numpy()[0][0], weights_layer[2][1].numpy()[0][1], 0, 0, 0,
                   weights_layer[2][1].numpy()[1][0], weights_layer[2][1].numpy()[1][1], 0, 0, 0,
                   0, 0, weights_layer[2][1].numpy()[0][0], weights_layer[2][1].numpy()[0][1], 0,
                   0, 0, weights_layer[2][1].numpy()[1][0], weights_layer[2][1].numpy()[1][1], 0,
                   0, 0, 0, 0, r_const]
    weights.append(weights_5_5)
    weights_5_3 = [weights_layer[3][1].numpy()[0][0], weights_layer[3][1].numpy()[0][1], 0, 0, 0,
                   0, 0, weights_layer[3][1].numpy()[0][0], weights_layer[3][1].numpy()[0][1], 0,
                   0, 0, 0, 0, r_const]
    weights.append(weights_5_3)
    weights_3_1 = [2.25, 2.25, - r_const * c.numpy()]
    weights.append(weights_3_1)
    weights_1_1 = [1]
    weights.append(weights_1_1)
    print("Layer cts: [3, 5, 5, 3, 1, 1]")
    print("Weights: ")
    for w in weights:
        print(w)
    print(weights)


if __name__ == '__main__':
    main()
