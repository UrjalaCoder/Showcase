import matplotlib.pyplot as plt
import numpy as np
import math, random

import os, sys

MAX_X = 10
MAX_Y = 10

MIN_X = -MAX_X
MIN_Y = -MAX_Y

SAMPLE_SIZE = 64

# We are trying to learn a linear equation y = Ax + B
A = random.randint(1, 1)
B = random.randint(1, 1)
# B = -57
def classifySample(sample):
    yVal = A * sample[0] + B

    # Check if sample Y value is lower than the linear equation
    if yVal > sample[1]:
        return -1
    else:
        return 1
    #
    # distance_from_ceiling = sample[1] / MAX_Y
    #
    # if random.random() < distance_from_ceiling:
    #     return 1
    # else:
    #     return -1

def plot_samples(samples):
    new_dataA = []
    new_dataB = []
    for s in range(len(samples)):
        if samples[s][2] == -1:
            new_dataA.append((samples[s][0], samples[s][1]))
        else:
            new_dataB.append((samples[s][0], samples[s][1]))

    # print(new_dataA)
    # print(new_dataB)

    dataAX = [i[0] for i in new_dataA]
    dataAY = [i[1] for i in new_dataA]

    dataBX = [i[0] for i in new_dataB]
    dataBY = [i[1] for i in new_dataB]
    return (dataAX, dataAY, dataBX, dataBY)

def generate_training_samples(amount):
    samples = []
    one_counter = 0
    while len(samples) < amount:
        new_x = random.uniform(MIN_X, MAX_X)
        new_y = random.uniform(MIN_Y, MAX_Y)
        sample = (new_x, new_y, classifySample((new_x, new_y)))
        samples.append(sample)

    for s in samples:
        if s[2] == 1:
            one_counter = one_counter + 1
    if one_counter == amount or one_counter <= 0:
        return []

    return np.array(samples)


def activation_function(inputs_and_weights, bias):
    weighted_sum = 0
    for element in inputs_and_weights:
        weighted_sum = weighted_sum + element[0] * element[1]
    weighted_sum = weighted_sum + bias
    if weighted_sum > 0:
        return 1
    else:
        return -1


def generate_training_line(weights, bias, step_size):
    y_values = []
    x = MIN_X
    x_vals = []

    while x <= MAX_X:
        y_values.append(-(weights[0] / weights[1]) * x - (bias / weights[1]))
        x_vals.append(x)
        x = x + step_size
    return (np.array(y_values), np.array(x_vals))

# plt.warnings.warn("", 0, stacklevel=1)
def train():
    global A, B

    current_sample_size = SAMPLE_SIZE
    plt.ion()
    fig = plt.figure()
    while True:
        A = random.uniform(-1, 1)
        B = random.uniform(MIN_Y, MAX_Y)
        ax = fig.add_subplot(111)

        samples = generate_training_samples(current_sample_size)
        if len(samples) == 0:
            # print("DEBUG!")
            continue
        weights = [random.uniform(-1, 1) for _ in range(2)]
        bias = random.uniform(-1, 1)
        sample_data = plot_samples(samples)
        # print(sample_data)
        ax.scatter(sample_data[0], sample_data[1], c='r', marker='s', label=classifySample((sample_data[0][0], sample_data[1][0])))
        ax.scatter(sample_data[2], sample_data[3], c='b', marker='o', label=classifySample((sample_data[2][0], sample_data[3][0])))
        plt.legend(loc="upper left")

        plt.axis([MIN_X, MAX_X, MIN_Y, MAX_Y])
        t, = ax.plot([], [], c='black')
        # w, = ax.plot([], [], marker='o', markersize=10, color='green')
        plt.plot([MIN_X, MAX_X], [A * MIN_X + B, A * MAX_X + B], c="green")
        MAX_COUNTER = 5000
        real_success = False
        counter = 0
        while not real_success and counter < MAX_COUNTER:
            success = True
            wrong_counter = 0
            for training_sample in samples:
                # training_sample = samples[random.randrange(0, len(samples))]
                x, y, correct_value = training_sample[0], training_sample[1], training_sample[2]
                inputs_and_weights = ([(x, weights[0]), (y, weights[1])])
                result = activation_function(inputs_and_weights, bias)

                if result != correct_value:
                    # Deltas for weights and bias.
                    deltaWeightX = correct_value * x
                    deltaWeightY = correct_value * y
                    deltaBias = correct_value

                    # Updating weights and bias.
                    weights[0] = weights[0] + deltaWeightX
                    weights[1] = weights[1] + deltaWeightY
                    bias = bias + deltaBias
                    counter = counter + 1
                    wrong_counter = wrong_counter + 1
                    success = False

            training_line_data = generate_training_line(weights, bias, 1)
            t.set_ydata(training_line_data[0])
            t.set_xdata(training_line_data[1])
            # w.set_ydata(weights[1])
            # w.set_xdata(weights[0])
            fig.canvas.draw()
            fig.canvas.flush_events()
            ax.set_title("counter: {} | success: {} | wrong point amount: {} | error percentage: {:.2f}".format(counter, real_success, wrong_counter, (wrong_counter / current_sample_size) * 100))
            real_success = success

        # print(min([current_sample_size * 2, 1000]))
        # current_sample_size = min([current_sample_size * 2, math.pow(2, 14)])

        plt.clf()
train()
