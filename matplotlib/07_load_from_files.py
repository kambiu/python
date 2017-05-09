import matplotlib.pyplot as plt
import csv
import numpy as np

# part1
"""
x = []
y = []

with open('07_example.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0])) # convert to float of int
        y.append(int(row[1]))
"""

# part2
x, y = np.loadtxt('07_example.txt', delimiter=',', unpack=True)

plt.plot(x,y, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()
