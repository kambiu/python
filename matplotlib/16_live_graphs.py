import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


style.use('fivethirtyeight')

fig = plt.figure()

# (1,1,1) --> subplot 1x1, the first one subplot
ax1 = fig.add_subplot(1,1,1)


def animate(i):
    graph_data = open('07_example.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)


ani = animation.FuncAnimation(fig, animate, interval=1000) # update the graphe every 1s
plt.show()


#to test, try to update 07_example.txt bny adding new rows to it