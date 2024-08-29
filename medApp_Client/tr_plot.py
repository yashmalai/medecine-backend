import matplotlib.pyplot as plt
import numpy as np


def ShowPlot(*args):
    plt.style.use('_mpl-gallery')

    data = [*args]
    n = len(data)
    x = np.sin(np.linspace(0, 2 * np.pi, n))
    y = np.cos(np.linspace(0, 2 * np.pi, n))
    z = [*args] #прием данных

    # Plot
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.stem(x, y, z)

    ax.set(xticklabels=[],
           yticklabels=[],
           zticklabels=[])
    plt.show()


if __name__ == '__main__':
    dat = [1, 3, 2, 5, 8, 6, 7, 4, 9, 10]
    ShowPlot(*dat)
