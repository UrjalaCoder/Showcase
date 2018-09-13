import numpy as np
import math, time
import matplotlib.pyplot as plt

MIN_X = -20
MAX_X = 20

MIN_Y = -20
MAX_Y = 20

M_RANGE = (-3, 3)
B_RANGE = (-70, 70)

AMOUNT = 50
MAX_DEVIATION = 5
LEARNING_RATE = 0.0001


def draw(data, figure):
    #
    # biggest_y = 0
    # lowest_y = 0
    # for row in data:
    #     if row[2] > biggest_y:
    #         biggest_y = row[2]
    #     if row[2] < lowest_y:
    #         lowest_y = row[2]

    ax = figure.add_subplot(111)
    ax.axis([MIN_X, MAX_X, -200, 200])
    line, = ax.plot([], [], 'r-')
    x = data[:, 1]
    y = data[:, np.shape(data)[1] - 1]
    ax.scatter(x, y)
    plt.show()
    return (line, figure)

def get_y(weights, input1):
    return np.dot(weights, np.asarray([1, input1]))

def update_line(weights, line, figure):
    # time.sleep(1/10)
    x = np.linspace(MIN_X, MAX_X, 1000)
    y = np.asarray([get_y(weights, i) for i in x])
    line.set_xdata(x)
    line.set_ydata(y)
    figure.canvas.draw()
    # time.sleep()
    return line


# training_data is in the format of [input, output]
def generate_training_data(m, b, MIN_X = 0, MAX_X = 10, amount = 20, max_deviation = 20):
    training_data = []
    # Get random distribution and sort in ascending order...
    x_vals = np.sort(np.random.uniform(MIN_X, MAX_X, amount), axis=None)

    # Round to two decimal places
    x_vals = np.around(x_vals, decimals=2)

    for x in x_vals:
        y = m * x + b
        # while y < MIN_Y or y > MAX_Y:
        #     y = m * x + b

        y = y + np.random.normal(y, max_deviation / 2)

        # To make the algorithm work x_0 needs to be 1
        training_data.append([1, x, y])
    return np.asarray(training_data)


def calculate_cost_function(training_data, weights):
    column_count = np.shape(training_data)[1]
    cost = 0
    for data in training_data:
        delta = np.dot(data[0:column_count - 1], weights) - data[column_count - 1]
        cost = cost + math.pow(delta, 2)
    return cost * 0.5

def linear_regression(training_data, figure):
    # Initialize weights to be zeroes
    weights = np.zeros(np.shape(training_data)[1] - 1)
    cost = calculate_cost_function(training_data, weights)
    print(weights, cost)
    counter = 0
    delta_cost = cost
    previous_cost = cost
    l, f = draw(training_data, figure)
    while counter < 10000 and abs(delta_cost) > 0.00005:
        weights = gradient_descent(weights, training_data, LEARNING_RATE)
        cost = calculate_cost_function(training_data, weights)
        delta_cost = previous_cost - cost
        previous_cost = cost
        print("delta cost: {}".format(delta_cost))
        # print("weights: " + str(weights))
        print("cost: " + str(cost))
        # print(training_data)
        if counter % 50 == 0:
            l = update_line(weights, l, f)
        # print(counter)
        counter = counter + 1
    print("Generating a new problem...")
    time.sleep(2)
    plt.clf()
    M = np.random.uniform(M_RANGE[0], M_RANGE[1])
    b = np.random.uniform(B_RANGE[0], B_RANGE[1])
    linear_regression(generate_training_data(M, b, MIN_X, MAX_X, amount=AMOUNT, max_deviation=MAX_DEVIATION), f)

"""
returns updated weights
"""
def gradient_descent(weights, training_data, training_rate):
    new_weights = []
    for weight_index in range(len(weights)):
        partial_derivative_sum = 0
        for data in training_data:
            # Dot product of weights and input vector
            inputs = data[0:len(data) - 1]
            hypotesis = np.dot(weights, inputs)
            # real value in the 3rd column
            correct_value = data[len(data) - 1]
            # input val for this weight index
            input_val = inputs[weight_index]

            partial_derivative_sum = partial_derivative_sum + (hypotesis - correct_value) * input_val

        # old weight value
        old_weight = weights[weight_index]

        # new weight
        weight = old_weight - (training_rate * partial_derivative_sum)
        new_weights.append(weight)

    return np.asarray(new_weights)

def main():
    M = np.random.uniform(M_RANGE[0], M_RANGE[1])
    b = np.random.uniform(B_RANGE[0], B_RANGE[1])

    print("{}x + {}".format(M, b))

    training_data = generate_training_data(M, b, MIN_X, MAX_X, amount=AMOUNT, max_deviation = MAX_DEVIATION)
    plt.ion()
    figure = plt.figure()
    # for data in training_data:
    #     print(data)
    linear_regression(training_data, figure)
if __name__ == "__main__":
    main()
